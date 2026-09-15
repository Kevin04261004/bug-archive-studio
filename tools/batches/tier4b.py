# -*- coding: utf-8 -*-
"""4티어 뒷부분: 생성자·구조체 초기화·인터페이스 선언·속성 접근자·static 클래스."""
from _common import make, write

E = {}
ep = make(E)

# 193 CS0768 — 두 생성자가 서로를 부른다.
ep('CS0768', 'Player.cs',
   "Constructor 'Player.Player(int)' cannot call itself through another constructor", """
using UnityEngine;

public class Player
{
    public int hp;

    public Player() : this(100)
    {
        Debug.Log("default");
    }

    public Player(int startHp) : this()
    {
        hp = startHp;
    }
}
""", """
using UnityEngine;

public class Player
{
    public int hp;

    public Player() : this(100)
    {
        Debug.Log("default");
    }

    public Player(int startHp)
    {
        hp = startHp;
    }
}
""", 12)

# 195 CS0522 — 구조체 생성자에 base() 를 붙였다.
ep('CS0522', 'Bag.cs',
   "'Slot.Slot(int)': structs cannot call base class constructors", """
using UnityEngine;

public struct Slot
{
    public int id;

    public Slot(int value) : base()
    {
        id = value;
    }
}

public class Bag : MonoBehaviour
{
    void Start()
    {
        Debug.Log(new Slot(1).id);
    }
}
""", """
using UnityEngine;

public struct Slot
{
    public int id;

    public Slot(int value)
    {
        id = value;
    }
}

public class Bag : MonoBehaviour
{
    void Start()
    {
        Debug.Log(new Slot(1).id);
    }
}
""", 7)

# 196 CS0514 — 정적 생성자에서 다른 생성자를 부르려 했다.
ep('CS0514', 'SaveTools.cs',
   "Static constructor 'SaveTools' cannot have an explicit this or base constructor call", """
using UnityEngine;

public class SaveTools
{
    public static int slot;

    static SaveTools() : this()
    {
        slot = 1;
    }

    public SaveTools()
    {
        Debug.Log("created");
    }
}
""", """
using UnityEngine;

public class SaveTools
{
    public static int slot;

    static SaveTools()
    {
        slot = 1;
    }

    public SaveTools()
    {
        Debug.Log("created");
    }
}
""", 7)

# 197 CS0515 — 정적 생성자에 public 을 붙였다.
ep('CS0515', 'SaveTools.cs',
   "'SaveTools.SaveTools()': access modifiers are not allowed on static constructors", """
using UnityEngine;

public class SaveTools
{
    public static int slot;

    public static SaveTools()
    {
        slot = 1;
    }

    public void Save()
    {
        Debug.Log(slot);
    }
}
""", """
using UnityEngine;

public class SaveTools
{
    public static int slot;

    static SaveTools()
    {
        slot = 1;
    }

    public void Save()
    {
        Debug.Log(slot);
    }
}
""", 7)

# 198 CS0132 — 정적 생성자에 매개변수를 넣었다.
ep('CS0132', 'SaveTools.cs',
   "'SaveTools.SaveTools(int)': a static constructor must be parameterless", """
using UnityEngine;

public class SaveTools
{
    public static int slot;

    static SaveTools(int start)
    {
        slot = 1;
    }

    public void Save()
    {
        Debug.Log(slot);
    }
}
""", """
using UnityEngine;

public class SaveTools
{
    public static int slot;

    static SaveTools()
    {
        slot = 1;
    }

    public void Save()
    {
        Debug.Log(slot);
    }
}
""", 7)

# 199 CS0171 — 구조체 생성자에서 필드 하나를 안 채웠다.
ep('CS0171', 'Bag.cs',
   "Field 'Slot.count' must be fully assigned before control is returned to the caller", """
using UnityEngine;

public struct Slot
{
    public int id;
    public int count;

    public Slot(int value)
    {
        id = value;

    }
}
public class Bag : MonoBehaviour
{
    void Start()
    {
        Debug.Log(new Slot(1).id);
    }
}
""", """
using UnityEngine;

public struct Slot
{
    public int id;
    public int count;

    public Slot(int value)
    {
        id = value;
        count = 0;
    }
}
public class Bag : MonoBehaviour
{
    void Start()
    {
        Debug.Log(new Slot(1).id);
    }
}
""", 11)

# 200 CS0188 — 필드를 채우기 전에 메서드를 불렀다.
ep('CS0188', 'Bag.cs',
   "The 'this' object cannot be used before all of its fields are assigned", """
using UnityEngine;

public struct Slot
{
    public int id;

    public Slot(int value)
    {

        Log();
    }

    void Log()
    {
        Debug.Log(id);
    }
}
""", """
using UnityEngine;

public struct Slot
{
    public int id;

    public Slot(int value)
    {
        id = value;
        Log();
    }

    void Log()
    {
        Debug.Log(id);
    }
}
""", 9)

# 201 CS0523 — 구조체가 자기 자신을 필드로 가진다.
ep('CS0523', 'Chain.cs',
   "Struct member 'Node.next' of type 'Node' causes a cycle in the struct layout", """
using UnityEngine;

public struct Node
{
    public int value;
    public Node next;
}

public class Chain : MonoBehaviour
{
    void Start()
    {
        Node head = default;
        Debug.Log(head.value);
    }
}
""", """
using UnityEngine;

public struct Node
{
    public int value;
    public Node[] next;
}

public class Chain : MonoBehaviour
{
    void Start()
    {
        Node head = default;
        Debug.Log(head.value);
    }
}
""", 6)

# 202 CS0525 — 인터페이스에 필드를 넣었다.
ep('CS0525', 'Unit.cs', "Interfaces cannot contain instance fields", """
using UnityEngine;

public interface IUnit
{
    int hp;

    void Hit(int amount);
}

public class Enemy : IUnit
{
    public int hp = 100;
    public int Hp => hp;

    public void Hit(int amount)
    {
        hp -= amount;
    }
}
""", """
using UnityEngine;

public interface IUnit
{
    int Hp { get; }

    void Hit(int amount);
}

public class Enemy : IUnit
{
    public int hp = 100;
    public int Hp => hp;

    public void Hit(int amount)
    {
        hp -= amount;
    }
}
""", 5)

# 203 CS0526 — 인터페이스에 생성자를 넣었다.
ep('CS0526', 'Unit.cs', "Interfaces cannot contain instance constructors", """
using UnityEngine;

public interface IUnit
{
    IUnit() { }

    void Hit(int amount);
}

public class Enemy : IUnit
{
    public int hp = 100;

    public void Hit(int amount)
    {
        hp -= amount;
    }
}
""", """
using UnityEngine;

public interface IUnit
{


    void Hit(int amount);
}

public class Enemy : IUnit
{
    public int hp = 100;

    public void Hit(int amount)
    {
        hp -= amount;
    }
}
""", 5)

# 204 CS0527 — 인터페이스 목록에 클래스를 적었다.
ep('CS0527', 'Ticker.cs',
   "Type 'Clock' in interface list is not an interface", """
using UnityEngine;

public class Clock
{
    public float time;
}

public interface ITick : Clock
{
    void Tick();
}

public class Spawner : ITick
{
    public void Tick() { }
}
""", """
using UnityEngine;

public class Clock
{
    public float time;
}

public interface ITick
{
    void Tick();
}

public class Spawner : ITick
{
    public void Tick() { }
}
""", 8)

# 205 CS0528 — 같은 인터페이스를 두 번 적었다.
ep('CS0528', 'Crate.cs', "'IDamage' is already listed in the interface list", """
using UnityEngine;

public interface IDamage
{
    void TakeHit(int amount);
}

public interface IMovable
{
    void Move();
}

public class Crate : IDamage, IDamage
{
    public void TakeHit(int amount) { }
    public void Move() { }
}
""", """
using UnityEngine;

public interface IDamage
{
    void TakeHit(int amount);
}

public interface IMovable
{
    void Move();
}

public class Crate : IDamage, IMovable
{
    public void TakeHit(int amount) { }
    public void Move() { }
}
""", 13)

# 206 CS0529 — 두 인터페이스가 서로를 상속한다.
ep('CS0529', 'Breakable.cs',
   "Inherited interface 'IBreak' causes a cycle in the interface hierarchy of 'IDamage'", """
using UnityEngine;

public interface IDamage : IBreak
{
    void TakeHit(int amount);
}

public interface IBreak : IDamage
{
    void Shatter();
}

public class Crate : IBreak
{
    public void TakeHit(int amount) { }
    public void Shatter() { }
}
""", """
using UnityEngine;

public interface IDamage
{
    void TakeHit(int amount);
}

public interface IBreak : IDamage
{
    void Shatter();
}

public class Crate : IBreak
{
    public void TakeHit(int amount) { }
    public void Shatter() { }
}
""", 3)

# 207 CS0146 — 두 클래스가 서로를 상속한다.
ep('CS0146', 'Hero.cs',
   "Circular base type dependency involving 'Boss' and 'Hero'", """
using UnityEngine;

public class Hero : Boss
{
    public int hp = 100;
}

public class Boss : Hero
{
    public int shield = 50;
}
""", """
using UnityEngine;

public class Hero : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Hero
{
    public int shield = 50;
}
""", 3)

# 209 CS0175 — base 만 단독으로 썼다.
ep('CS0175', 'Boss.cs',
   "Use of keyword 'base' is not valid in this context", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Enemy
{
    void Show()
    {
        Debug.Log(base);
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Enemy
{
    void Show()
    {
        Debug.Log(base.hp);
    }
}
""", 12)

# 210 CS1511 — static 메서드에서 base 를 썼다.
ep('CS1511', 'Boss.cs',
   "Keyword 'base' is not available in a static method", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public void ResetHp() { }
}

public class Boss : Enemy
{
    static void ResetAll()
    {
        base.ResetHp();
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public void ResetHp() { }
}

public class Boss : Enemy
{
    void ResetAll()
    {
        base.ResetHp();
    }
}
""", 10)

# 211 CS1512 — static 필드 초기화에서 base 를 썼다.
ep('CS1512', 'Boss.cs',
   "Keyword 'base' is not available in the current context", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Enemy
{
    static int copy = base.hp;

    void Show()
    {
        Debug.Log(copy);
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Enemy
{
    static int copy = 100;

    void Show()
    {
        Debug.Log(copy);
    }
}
""", 10)

# 212 CS0205 — 본문이 없는 추상 멤버를 base 로 불렀다.
ep('CS0205', 'Boss.cs',
   "Cannot call an abstract base member: 'Enemy.Hit()'", """
using UnityEngine;

public abstract class Enemy
{
    public abstract void Hit();
}

public class Boss : Enemy
{
    public int hp = 100;

    public override void Hit()
    {
        base.Hit();
        hp -= 10;
    }
}
""", """
using UnityEngine;

public abstract class Enemy
{
    public abstract void Hit();
}

public class Boss : Enemy
{
    public int hp = 100;

    public override void Hit()
    {
        Debug.Log("boss hit");
        hp -= 10;
    }
}
""", 14)

# 213 CS0026 — static 메서드에서 this 를 썼다.
ep('CS0026', 'Player.cs',
   "Keyword 'this' is not valid in a static property, static method, or static field", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    static void ResetAll()
    {
        this.hp = 0;
        Debug.Log("reset");
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    void ResetAll()
    {
        this.hp = 0;
        Debug.Log("reset");
    }
}
""", 7)

# 214 CS0027 — 필드 초기화에서 this 를 썼다.
ep('CS0027', 'Player.cs',
   "Keyword 'this' is not available in the current context", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;
    public int copy = this.hp;

    void Start()
    {
        Debug.Log(copy);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;
    public int copy = 100;

    void Start()
    {
        Debug.Log(copy);
    }
}
""", 6)

# 215 CS0236 — 필드 초기화에서 다른 필드를 썼다.
ep('CS0236', 'Player.cs',
   "A field initializer cannot reference the non-static field 'hp'", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;
    public int shield = hp / 2;

    void Start()
    {
        Debug.Log(shield);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;
    public int shield = 50;

    void Start()
    {
        Debug.Log(shield);
    }
}
""", 6)

# 216 CS0154 — set 만 만든 속성을 읽었다.
ep('CS0154', 'Player.cs',
   "The property 'Player.Hp' cannot be used in this context; it lacks the get accessor", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp = 100;

    public int Hp { set { hp = value; } }

    void Start()
    {
        Debug.Log(Hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp = 100;

    public int Hp { get { return hp; } }

    void Start()
    {
        Debug.Log(Hp);
    }
}
""", 7)

# 217 CS0271 — get 을 private 로 막아두고 밖에서 읽었다.
ep('CS0271', 'Bag.cs',
   "The property 'Player.Hp' cannot be used here; the get accessor is inaccessible", """
using UnityEngine;

public class Player
{
    public int Hp { private get; set; }
}

public class Bag : MonoBehaviour
{
    public Player target;

    void Start()
    {
        Debug.Log(target.Hp);
    }
}
""", """
using UnityEngine;

public class Player
{
    public int Hp { get; set; }
}

public class Bag : MonoBehaviour
{
    public Player target;

    void Start()
    {
        Debug.Log(target.Hp);
    }
}
""", 5)

# 218 CS0272 — set 을 private 로 막아두고 밖에서 넣었다.
ep('CS0272', 'Bag.cs',
   "The property 'Player.Hp' cannot be used here; the set accessor is inaccessible", """
using UnityEngine;

public class Player
{
    public int Hp { get; private set; }
}

public class Bag : MonoBehaviour
{
    public Player target;

    void Start()
    {
        target.Hp = 5;
    }
}
""", """
using UnityEngine;

public class Player
{
    public int Hp { get; set; }
}

public class Bag : MonoBehaviour
{
    public Player target;

    void Start()
    {
        target.Hp = 5;
    }
}
""", 5)

# 219 CS0273 — 접근자를 속성보다 넓게 열었다.
ep('CS0273', 'Player.cs',
   "The accessibility modifier of 'Player.Hp.set' must be more restrictive", """
using UnityEngine;

public class Player : MonoBehaviour
{
    private int Hp { get; public set; }

    void Start()
    {
        Hp = 100;
        Debug.Log(Hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int Hp { get; private set; }

    void Start()
    {
        Hp = 100;
        Debug.Log(Hp);
    }
}
""", 5)

# 220 CS0274 — 접근자 둘 다에 한정자를 붙였다.
ep('CS0274', 'Player.cs',
   "Cannot specify accessibility modifiers for both accessors of 'Player.Hp'", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int Hp
    {
        private get;
        private set;
    }

    void Start()
    {
        Hp = 100;
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int Hp
    {
        get;
        private set;
    }

    void Start()
    {
        Hp = 100;
    }
}
""", 7)

# 221 CS0276 — 접근자가 하나뿐인데 한정자를 붙였다.
ep('CS0276', 'Player.cs',
   "'Player.Hp': accessibility modifiers may only be used if it has both get and set", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp = 100;

    public int Hp { private get; }

    void Start()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp = 100;

    public int Hp { get; }

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 7)

# 222 CS0442 — 추상 속성의 접근자를 private 로 막았다.
ep('CS0442', 'Unit.cs',
   "'Unit.Hp': abstract properties cannot have private accessors", """
using UnityEngine;

public abstract class Unit
{
    public abstract int Hp
    {
        get;
        private set;
    }
}

public class Enemy : Unit
{
    public override int Hp { get; set; }
}
""", """
using UnityEngine;

public abstract class Unit
{
    public abstract int Hp
    {
        get;
        set;
    }
}

public class Enemy : Unit
{
    public override int Hp { get; set; }
}
""", 8)

# 223 CS0547 — 속성 타입을 void 로 적었다.
ep('CS0547', 'Player.cs',
   "'Player.Hp': property or indexer cannot have void type", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public void Hp { get; set; }

    void Start()
    {
        Hp = 100;
        Debug.Log(Hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int Hp { get; set; }

    void Start()
    {
        Hp = 100;
        Debug.Log(Hp);
    }
}
""", 5)

# 224 CS0548 — 접근자를 하나도 안 넣었다.
ep('CS0548', 'Player.cs',
   "'Player.Hp': property or indexer must have at least one accessor", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int Hp { }

    void Start()
    {
        Debug.Log(Hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int Hp { get; set; }

    void Start()
    {
        Debug.Log(Hp);
    }
}
""", 5)

# 225 CS0550 — 인터페이스에 없는 set 을 명시적 구현에 넣었다.
ep('CS0550', 'Enemy.cs',
   "'Enemy.IHealth.Hp.set' adds an accessor not found in interface member 'IHealth.Hp'", """
using UnityEngine;

public interface IHealth
{
    int Hp { get; }
}

public class Enemy : IHealth
{
    int IHealth.Hp { get; set; }

    void Log()
    {
        Debug.Log("hp");
    }
}
""", """
using UnityEngine;

public interface IHealth
{
    int Hp { get; }
}

public class Enemy : IHealth
{
    int IHealth.Hp { get; }

    void Log()
    {
        Debug.Log("hp");
    }
}
""", 10)

# 226 CS0551 — 명시적 구현에서 set 을 빠뜨렸다.
ep('CS0551', 'Enemy.cs',
   "Explicit interface implementation 'Enemy.IHealth.Hp' is missing accessor", """
using UnityEngine;

public interface IHealth
{
    int Hp { get; set; }
}

public class Enemy : IHealth
{
    int IHealth.Hp { get; }

    void Log()
    {
        Debug.Log("hp");
    }
}
""", """
using UnityEngine;

public interface IHealth
{
    int Hp { get; set; }
}

public class Enemy : IHealth
{
    int IHealth.Hp { get; set; }

    void Log()
    {
        Debug.Log("hp");
    }
}
""", 10)

# 227 CS1551 — 인덱서에 매개변수를 안 넣었다.
ep('CS1551', 'Inventory.cs',
   "An indexer must have at least one parameter", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    int[] slots = new int[9];

    public int this[] => slots[0];

    void Start()
    {
        Debug.Log(slots[0]);
    }
}
""", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    int[] slots = new int[9];

    public int this[int i] => slots[i];

    void Start()
    {
        Debug.Log(slots[0]);
    }
}
""", 7)

# 228 CS0620 — 인덱서 타입을 void 로 적었다.
ep('CS0620', 'Inventory.cs', "Indexers cannot have void type", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    int[] slots = new int[9];

    public void this[int i]
    {
        get { return slots[i]; }
    }

    void Start()
    {
        Debug.Log(slots[0]);
    }
}
""", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    int[] slots = new int[9];

    public int this[int i]
    {
        get { return slots[i]; }
    }

    void Start()
    {
        Debug.Log(slots[0]);
    }
}
""", 7)

# 229 CS0621 — virtual 멤버를 private 로 막았다.
ep('CS0621', 'Enemy.cs',
   "'Enemy.Hit()': virtual or abstract members cannot be private", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    private virtual void Hit()
    {
        hp -= 10;
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    protected virtual void Hit()
    {
        hp -= 10;
    }
}
""", 7)

# 230 CS0708 — static 클래스에 인스턴스 필드를 뒀다.
ep('CS0708', 'SaveTools.cs',
   "'SaveTools.slot': cannot declare instance members in a static class", """
using UnityEngine;

public static class SaveTools
{
    public int slot;
    public static string path = "save";

    public static void Save()
    {
        Debug.Log(path);
    }
}
""", """
using UnityEngine;

public static class SaveTools
{
    public static int slot;
    public static string path = "save";

    public static void Save()
    {
        Debug.Log(path);
    }
}
""", 5)

# 231 CS0709 — static 클래스를 상속했다.
ep('CS0709', 'CloudSave.cs',
   "'CloudSave': cannot derive from static class 'SaveTools'", """
using UnityEngine;

public static class SaveTools
{
    public static string path = "save";
}

public class CloudSave : SaveTools
{
    public int slot;
}
""", """
using UnityEngine;

public static class SaveTools
{
    public static string path = "save";
}

public class CloudSave
{
    public int slot;
}
""", 8)

# 232 CS0710 — static 클래스에 인스턴스 생성자를 뒀다.
ep('CS0710', 'SaveTools.cs',
   "Static classes cannot have instance constructors", """
using UnityEngine;

public static class SaveTools
{
    public static string path = "save";

    internal SaveTools()
    {
        Debug.Log("created");
    }
}
""", """
using UnityEngine;

public static class SaveTools
{
    public static string path = "save";

    static SaveTools()
    {
        Debug.Log("created");
    }
}
""", 7)

# 233 CS0712 — static 클래스를 new 했다.
ep('CS0712', 'Game.cs',
   "Cannot create an instance of the static class 'SaveTools'", """
using UnityEngine;

public static class SaveTools
{
    public static void Save()
    {
        Debug.Log("saved");
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        var tools = new SaveTools();
        Debug.Log("done");
    }
}
""", """
using UnityEngine;

public static class SaveTools
{
    public static void Save()
    {
        Debug.Log("saved");
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        SaveTools.Save();
        Debug.Log("done");
    }
}
""", 15)

# 234 CS0713 — static 클래스를 다른 타입에서 파생시켰다.
ep('CS0713', 'SaveTools.cs',
   "Static class 'SaveTools' cannot derive from type 'Storage'", """
using UnityEngine;

public class Storage
{
    public string path = "save";
}

public static class SaveTools : Storage
{
    public static void Save()
    {
        Debug.Log("saved");
    }
}
""", """
using UnityEngine;

public class Storage
{
    public string path = "save";
}

public static class SaveTools
{
    public static void Save()
    {
        Debug.Log("saved");
    }
}
""", 8)

if __name__ == '__main__':
    write(E, 'tier4b.json')
