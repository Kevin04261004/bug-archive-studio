# -*- coding: utf-8 -*-
"""9티어: 어트리뷰트·연산자 오버로딩·사용자 정의 변환·fixed 버퍼·별칭."""
from _common import make, write

E = {}
ep = make(E)

ep('CS0028', 'Program.cs',
   "'Program.Main(string)' has the wrong signature to be an entry point", """
using System;

class Program
{
    static int Main(string args)
    {
        Console.WriteLine("start");
        return 0;
    }
}
""", """
using System;

class Program
{
    static int Main(string[] args)
    {
        Console.WriteLine("start");
        return 0;
    }
}
""", 5)

ep('CS0181', 'Hint.cs',
   "Attribute constructor parameter 'weight' has type 'decimal', which is not valid", """
using System;

public class Hint : Attribute
{
    public Hint(decimal weight) { }
}

[Hint(1)]
public class Player
{
    public int hp = 100;
}
""", """
using System;

public class Hint : Attribute
{
    public Hint(int weight) { }
}

[Hint(1)]
public class Player
{
    public int hp = 100;
}
""", 5)

ep('CS0182', 'Hint.cs',
   "An attribute argument must be a constant expression, typeof or array creation", """
using System;

public class Hint : Attribute
{
    public Hint(int weight) { }
}

[Hint(DateTime.Now.Year)]
public class Player
{
    public int hp = 100;
}
""", """
using System;

public class Hint : Attribute
{
    public Hint(int weight) { }
}

[Hint(2026)]
public class Player
{
    public int hp = 100;
}
""", 8)

ep('CS0215', 'Gold.cs',
   "The return type of operator true or operator false must be bool", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static int operator true(
        Gold coin) => default;

    public static bool operator false(
        Gold coin) => default;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static bool operator true(
        Gold coin) => default;

    public static bool operator false(
        Gold coin) => default;
}
""", 7)

ep('CS0216', 'Gold.cs',
   "The operator 'Gold.operator ==(Gold, Gold)' requires a matching operator '!='", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static bool operator ==(
        Gold left, Gold right) => true;

    public static bool operator <(
        Gold left, Gold right) => false;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static bool operator ==(
        Gold left, Gold right) => true;

    public static bool operator !=(
        Gold left, Gold right) => false;
}
""", 10)

ep('CS0233', 'Bag.cs',
   "'Slot' does not have a predefined size, so sizeof needs an unsafe context", """
using UnityEngine;

public struct Slot
{
    public int id;
}

public class Bag : MonoBehaviour
{
    void Start()
    {
        Debug.Log(sizeof(Slot));
    }
}
""", """
using UnityEngine;

public struct Slot
{
    public int id;
}

public class Bag : MonoBehaviour
{
    unsafe void Start()
    {
        Debug.Log(sizeof(Slot));
    }
}
""", 10)

ep('CS0430', 'Game.cs',
   "The extern alias 'Lib' was not specified in a reference option", """
extern alias Lib;
using UnityEngine;

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log("start");
    }
}
""", """

using UnityEngine;

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log("start");
    }
}
""", 1)

ep('CS0432', 'Game.cs', "Alias 'Lib' not found", """
using UnityEngine;

public class Game : MonoBehaviour
{
    public int level = 1;

    void Start()
    {
        Lib::Debug.Log("start");
    }
}
""", """
using UnityEngine;

public class Game : MonoBehaviour
{
    public int level = 1;

    void Start()
    {
        Debug.Log("start");
    }
}
""", 9)

ep('CS0439', 'Game.cs',
   "An extern alias declaration must precede all other elements", """
extern alias Lib;
using UnityEngine;
extern alias Other;

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log("start");
    }
}
""", """
extern alias Lib;
using UnityEngine;


public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log("start");
    }
}
""", 3)

ep('CS0448', 'Gold.cs',
   "The return type for the ++ or -- operator must match the parameter type", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static int operator ++(
        Gold coin) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator ++(
        Gold coin) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 7)

ep('CS0552', 'Gold.cs',
   "User-defined conversions to or from an interface are not allowed", """
using UnityEngine;

public interface ICoin { }

public struct Gold
{
    public int amount;

    public static implicit operator
        ICoin(Gold coin) => null;
}
""", """
using UnityEngine;

public interface ICoin { }

public struct Gold
{
    public int amount;

    public static implicit operator
        int(Gold coin) => 0;
}
""", 10)

ep('CS0553', 'Gold.cs',
   "User-defined conversion from a base class is not allowed", """
using UnityEngine;

public class Currency
{
    public int amount;
}

public class Gold : Currency
{
    public static implicit operator
        Gold(Currency raw) => null;
}
""", """
using UnityEngine;

public class Currency
{
    public int amount;
}

public class Gold : Currency
{
    public static implicit operator
        Gold(int raw) => null;
}
""", 11)

ep('CS0554', 'Currency.cs',
   "User-defined conversion from a derived class is not allowed", """
using UnityEngine;

public class Currency
{
    public static implicit operator
        Currency(Gold coin) => null;
}

public class Gold : Currency
{
    public int amount;
}
""", """
using UnityEngine;

public class Currency
{
    public static implicit operator
        Currency(int raw) => null;
}

public class Gold : Currency
{
    public int amount;
}
""", 6)

ep('CS0555', 'Gold.cs',
   "User-defined conversion cannot convert the enclosing type to itself", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static implicit operator
        Gold(Gold coin) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static implicit operator
        Gold(int raw) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 8)

ep('CS0556', 'Gold.cs',
   "User-defined conversion must convert to or from the enclosing type", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static implicit operator
        int(string raw) => 0;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static implicit operator
        int(Gold coin) => 0;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 8)

ep('CS0557', 'Gold.cs',
   "Duplicate user-defined conversion in type 'Gold'", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static implicit operator
        int(Gold coin) => 0;

    public static explicit operator
        int(Gold coin) => 1;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static implicit operator
        int(Gold coin) => 0;

    public static explicit operator
        float(Gold coin) => 1;
}
""", 11)

ep('CS0558', 'Gold.cs',
   "User-defined operator 'Gold.operator +(Gold, Gold)' must be static and public", """
using UnityEngine;

public struct Gold
{
    public int amount;

    static Gold operator +(
        Gold left, Gold right) => left;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator +(
        Gold left, Gold right) => left;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 7)

ep('CS0559', 'Gold.cs',
   "The parameter type for the ++ or -- operator must be the containing type", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator ++(
        int raw) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator ++(
        Gold coin) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 8)

ep('CS0562', 'Gold.cs',
   "The parameter of a unary operator must be the containing type", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator -(
        int raw) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator -(
        Gold coin) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 8)

ep('CS0563', 'Gold.cs',
   "One of the parameters of a binary operator must be the containing type", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator +(
        int left, int right) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator +(
        Gold left, int right) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 8)

ep('CS0564', 'Gold.cs',
   "The first operand of an overloaded shift operator must be the containing type", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator <<(
        int shift, int by) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator <<(
        Gold coin, int by) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 8)

ep('CS0576', 'Game.cs',
   "Namespace contains a definition conflicting with alias 'Player'", """
using Player = System.String;
using UnityEngine;

public class Player
{
    public int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start() { }
}
""", """

using UnityEngine;

public class Player
{
    public int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start() { }
}
""", 1)

ep('CS0577', 'Player.cs',
   "The Conditional attribute is not valid on a constructor", """
using System.Diagnostics;
using UnityEngine;

public class Player
{
    public int hp = 100;

    [Conditional("DEBUG")]
    public Player()
    {
        hp = 100;
    }
}
""", """
using System.Diagnostics;
using UnityEngine;

public class Player
{
    public int hp = 100;


    public Player()
    {
        hp = 100;
    }
}
""", 8)

ep('CS0578', 'Player.cs',
   "The Conditional attribute is not valid because the return type is not void", """
using System.Diagnostics;
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    [Conditional("DEBUG")]
    public int LogHp() => hp;

    void Start()
    {
        LogHp();
    }
}
""", """
using System.Diagnostics;
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    [Conditional("DEBUG")]
    public void LogHp() => Debug.Log(hp);

    void Start()
    {
        LogHp();
    }
}
""", 9)

ep('CS0579', 'Player.cs', "Duplicate 'Hint' attribute", """
using System;

public class Hint : Attribute { }

[Hint]
[Hint]
public class Player
{
    public int hp = 100;
}
""", """
using System;

public class Hint : Attribute { }

[Hint]

public class Player
{
    public int hp = 100;
}
""", 6)

ep('CS0582', 'Unit.cs',
   "The Conditional attribute is not valid on interface members", """
using System.Diagnostics;
using UnityEngine;

public interface IHit
{
    [Conditional("DEBUG")]
    void Hit();
}

public class Boss : IHit
{
    public void Hit() { }
}
""", """
using System.Diagnostics;
using UnityEngine;

public interface IHit
{

    void Hit();
}

public class Boss : IHit
{
    public void Hit() { }
}
""", 6)

ep('CS0590', 'Gold.cs', "User-defined operators cannot return void", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static void operator +(
        Gold left, Gold right) => left;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator +(
        Gold left, Gold right) => left;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 7)

ep('CS0592', 'Player.cs',
   "Attribute 'Hint' is not valid on this declaration type", """
using System;
using UnityEngine;

[AttributeUsage(AttributeTargets.Class)]
public class Hint : Attribute { }

public class Player : MonoBehaviour
{
    [Hint]
    public int hp = 100;
}
""", """
using System;
using UnityEngine;

[AttributeUsage(AttributeTargets.Field)]
public class Hint : Attribute { }

public class Player : MonoBehaviour
{
    [Hint]
    public int hp = 100;
}
""", 4)

ep('CS0596', 'Native.cs',
   "The ComImport attribute must be specified on the interface that has a Guid", """
using System.Runtime.InteropServices;


[Guid(
    "00000000-0000-0000-0000-000000000000")]
public interface IThing
{
    void Run();
}

public class Host
{
    IThing thing;
}
""", """
using System.Runtime.InteropServices;

[ComImport]
[Guid(
    "00000000-0000-0000-0000-000000000000")]
public interface IThing
{
    void Run();
}

public class Host
{
    IThing thing;
}
""", 3)

ep('CS0601', 'Native.cs',
   "The DllImport attribute must be specified on a method marked static and extern", """
using System.Runtime.InteropServices;
using UnityEngine;

public class Native : MonoBehaviour
{
    [DllImport("user32.dll")]
    public void Beep() { }

    void Start()
    {
        Beep();
    }
}
""", """
using System.Runtime.InteropServices;
using UnityEngine;

public class Native : MonoBehaviour
{
    [DllImport("user32.dll")]
    public static extern void Beep();

    void Start()
    {
        Beep();
    }
}
""", 7)

ep('CS0610', 'Player.cs',
   "Field or property cannot be of type 'System.TypedReference'", """
using System;
using UnityEngine;

public class Player : MonoBehaviour
{
    public TypedReference raw;
    public int hp = 100;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", """
using System;
using UnityEngine;

public class Player : MonoBehaviour
{
    public object raw;
    public int hp = 100;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 6)

ep('CS0611', 'Player.cs',
   "Array elements cannot be of type 'System.TypedReference'", """
using System;
using UnityEngine;

public class Player : MonoBehaviour
{
    void Start()
    {
        var raw = new TypedReference[2];
        Debug.Log(raw.Length);
    }
}
""", """
using System;
using UnityEngine;

public class Player : MonoBehaviour
{
    void Start()
    {
        var raw = new object[2];
        Debug.Log(raw.Length);
    }
}
""", 8)

ep('CS0616', 'Player.cs', "'Hint' is not an attribute class", """
using UnityEngine;

public class Hint { }

[Hint]
public class Player : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public class Hint : System.Attribute { }

[Hint]
public class Player : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 3)

ep('CS0617', 'Hint.cs',
   "'weight' is not a valid named attribute argument; it must not be readonly", """
using System;

public class Hint : Attribute
{
    public readonly int weight;
}

[Hint(weight = 1)]
public class Player
{
    public int hp = 100;
}
""", """
using System;

public class Hint : Attribute
{
    public int weight;
}

[Hint(weight = 1)]
public class Player
{
    public int hp = 100;
}
""", 5)

ep('CS0625', 'Packet.cs',
   "Instance field 'Packet.id' must have a FieldOffset attribute", """
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Explicit)]
public struct Packet
{

    public int id;
}

public class Host
{
    Packet packet;
}
""", """
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Explicit)]
public struct Packet
{
    [FieldOffset(0)]
    public int id;
}

public class Host
{
    Packet packet;
}
""", 6)

ep('CS0636', 'Packet.cs',
   "The FieldOffset attribute is only valid on types marked StructLayout(Explicit)", """
using System.Runtime.InteropServices;


public struct Packet
{
    [FieldOffset(0)]
    public int id;
}

public class Host
{
    Packet packet;
}
""", """
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Explicit)]
public struct Packet
{
    [FieldOffset(0)]
    public int id;
}

public class Host
{
    Packet packet;
}
""", 3)

ep('CS0637', 'Packet.cs',
   "The FieldOffset attribute is not allowed on static or const fields", """
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Explicit)]
public struct Packet
{
    [FieldOffset(0)]
    public static int id;
}

public class Host
{
    Packet packet;
}
""", """
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Explicit)]
public struct Packet
{
    [FieldOffset(0)]
    public int id;
}

public class Host
{
    Packet packet;
}
""", 7)

ep('CS0641', 'Hint.cs',
   "Attribute 'AttributeUsage' is only valid on classes derived from System.Attribute", """
using System;

[AttributeUsage(AttributeTargets.Class)]
public class Hint { }

[Hint]
public class Player
{
    public int hp = 100;
}
""", """
using System;

[AttributeUsage(AttributeTargets.Class)]
public class Hint : Attribute { }

[Hint]
public class Player
{
    public int hp = 100;
}
""", 4)

ep('CS0643', 'Hint.cs', "'weight' duplicate named attribute argument", """
using System;

public class Hint : Attribute
{
    public int weight;
    public int order;
}

[Hint(weight = 1, weight = 2)]
public class Player
{
    public int hp = 100;
}
""", """
using System;

public class Hint : Attribute
{
    public int weight;
    public int order;
}

[Hint(weight = 1, order = 2)]
public class Player
{
    public int hp = 100;
}
""", 9)

ep('CS0653', 'Hint.cs',
   "Cannot apply attribute class 'Hint' because it is abstract", """
using System;

public abstract class Hint : Attribute { }

[Hint]
public class Player
{
    public int hp = 100;
    public int mana = 50;
}
""", """
using System;

public class Hint : Attribute { }

[Hint]
public class Player
{
    public int hp = 100;
    public int mana = 50;
}
""", 3)

ep('CS0668', 'Inventory.cs',
   "Two indexers have different names; IndexerName must match within a type", """
using System.Runtime.CompilerServices;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    [IndexerName("Slot")]
    public int this[int index] => 0;

    [IndexerName("Item")]
    public int this[string name] => 0;
}
""", """
using System.Runtime.CompilerServices;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    [IndexerName("Slot")]
    public int this[int index] => 0;

    [IndexerName("Slot")]
    public int this[string name] => 0;
}
""", 9)

ep('CS0670', 'Player.cs', "Field cannot have void type", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public void hp;
    public int mana = 50;

    void Start()
    {
        Debug.Log(mana);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp;
    public int mana = 50;

    void Start()
    {
        Debug.Log(mana);
    }
}
""", 5)

ep('CS0673', 'Player.cs',
   "System.Void cannot be used from C#; use typeof(void) instead", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public System.Void raw;
    public int mana = 50;

    void Start()
    {
        Debug.Log(mana);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public object raw;
    public int mana = 50;

    void Start()
    {
        Debug.Log(mana);
    }
}
""", 5)

ep('CS0677', 'Counter.cs',
   "'Counter.hits': a volatile field cannot be of the type 'long'", """
using UnityEngine;

public class Counter : MonoBehaviour
{
    public volatile long hits;
    public int level = 1;

    void Start()
    {
        Debug.Log(level);
    }
}
""", """
using UnityEngine;

public class Counter : MonoBehaviour
{
    public volatile int hits;
    public int level = 1;

    void Start()
    {
        Debug.Log(level);
    }
}
""", 5)

ep('CS0678', 'Counter.cs',
   "'Counter.hits': a field cannot be both volatile and readonly", """
using UnityEngine;

public class Counter : MonoBehaviour
{
    public volatile readonly int hits;
    public int level = 1;

    void Start()
    {
        Debug.Log(level);
    }
}
""", """
using UnityEngine;

public class Counter : MonoBehaviour
{
    public volatile int hits;
    public int level = 1;

    void Start()
    {
        Debug.Log(level);
    }
}
""", 5)

ep('CS0681', 'Unit.cs',
   "The modifier 'abstract' is not valid on fields; try using a property instead", """
using UnityEngine;

public abstract class Unit
{
    public abstract int hp;
    public int mana = 50;

    public void Log()
    {
        Debug.Log(mana);
    }
}
""", """
using UnityEngine;

public abstract class Unit
{
    public abstract int hp { get; }
    public int mana = 50;

    public void Log()
    {
        Debug.Log(mana);
    }
}
""", 5)

ep('CS0687', 'Game.cs',
   "The namespace alias qualifier '::' always resolves to a type or namespace", """
using UnityEngine;

public class Player
{
    public static int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(Player::hp);
    }
}
""", """
using UnityEngine;

public class Player
{
    public static int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(Player.hp);
    }
}
""", 12)

ep('CS1019', 'Gold.cs', "Overloadable unary operator expected", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator /(
        Gold coin) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator -(
        Gold coin) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 7)

ep('CS1020', 'Gold.cs', "Overloadable binary operator expected", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator +=(
        Gold left, Gold right) => left;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator +(
        Gold left, Gold right) => left;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 7)

ep('CS1037', 'Gold.cs', "Overloadable operator expected", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator =(
        Gold left, Gold right) => left;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator +(
        Gold left, Gold right) => left;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 7)

ep('CS1534', 'Gold.cs',
   "Overloaded binary operator '+' takes two parameters", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator +(
        Gold coin) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator +(
        Gold left, Gold right) => left;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 8)

ep('CS1535', 'Gold.cs',
   "Overloaded unary operator '!' takes one parameter", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator !(
        Gold left, Gold right) => left;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator !(
        Gold coin) => default;
}

public class Wallet : MonoBehaviour
{
    Gold coins;
}
""", 8)

ep('CS1537', 'Game.cs',
   "The using alias 'Text' appeared previously in this namespace", """
using Text = System.Text;
using Text = System.IO;
using UnityEngine;

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log("start");
    }
}
""", """
using Text = System.Text;
using IO = System.IO;
using UnityEngine;

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log("start");
    }
}
""", 2)

ep('CS1558', 'Program.cs',
   "'Program' does not have a suitable static Main method", """
using System;

class Program
{
    public int hp = 100;

    void Main()
    {
        Console.WriteLine("start");
    }
}
""", """
using System;

class Program
{
    public int hp = 100;

    static void Main()
    {
        Console.WriteLine("start");
    }
}
""", 7)

ep('CS1575', 'Pixels.cs',
   "A stackalloc expression requires [] after type", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    public int width = 4;

    unsafe void Scan()
    {
        int* buffer = stackalloc int;
        Debug.Log(width);
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    public int width = 4;

    unsafe void Scan()
    {
        int* buffer = stackalloc int[4];
        Debug.Log(width);
    }
}
""", 9)

ep('CS1641', 'Buffer.cs',
   "A fixed size buffer field must have the array size specifier after the field name", """
using UnityEngine;

public unsafe struct Buffer
{
    public fixed int data;
}

public class Audio : MonoBehaviour
{
    public int rate = 44100;
}
""", """
using UnityEngine;

public unsafe struct Buffer
{
    public fixed int data[4];
}

public class Audio : MonoBehaviour
{
    public int rate = 44100;
}
""", 5)

ep('CS1642', 'Buffer.cs',
   "Fixed size buffer fields may only be members of structs", """
using UnityEngine;

public unsafe class Buffer
{
    public fixed int data[4];
}

public class Audio : MonoBehaviour
{
    public int rate = 44100;
}
""", """
using UnityEngine;

public unsafe struct Buffer
{
    public fixed int data[4];
}

public class Audio : MonoBehaviour
{
    public int rate = 44100;
}
""", 3)

ep('CS1663', 'Buffer.cs',
   "Fixed size buffer type must be a primitive type such as int, char or float", """
using UnityEngine;

public unsafe struct Buffer
{
    public fixed string data[4];
}

public class Audio : MonoBehaviour
{
    public int rate = 44100;
}
""", """
using UnityEngine;

public unsafe struct Buffer
{
    public fixed int data[4];
}

public class Audio : MonoBehaviour
{
    public int rate = 44100;
}
""", 5)

ep('CS1665', 'Buffer.cs',
   "Fixed size buffers must have a length greater than zero", """
using UnityEngine;

public unsafe struct Buffer
{
    public fixed int data[0];
}

public class Audio : MonoBehaviour
{
    public int rate = 44100;
}
""", """
using UnityEngine;

public unsafe struct Buffer
{
    public fixed int data[4];
}

public class Audio : MonoBehaviour
{
    public int rate = 44100;
}
""", 5)

ep('CS1686', 'Pixels.cs',
   "Local 'count' cannot have its address taken and be used inside a lambda expression", """
using System;
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int count = 1;
        int* raw = &count;
        Action log = () =>
            Debug.Log(count);
    }
}
""", """
using System;
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int count = 1;
        int* raw = &count;
        Action log = () =>
            Debug.Log(1);
    }
}
""", 11)

if __name__ == '__main__':
    write(E, 'tier9.json')
