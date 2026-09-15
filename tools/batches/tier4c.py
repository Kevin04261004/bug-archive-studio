# -*- coding: utf-8 -*-
"""static 클래스·이벤트·델리게이트·소멸자·partial·모호한 참조."""
from _common import make, write

E = {}
ep = make(E)

# 235 CS0714 — static 클래스에 인터페이스를 붙였다.
ep('CS0714', 'SaveTools.cs',
   "'SaveTools': static classes cannot implement interfaces", """
using UnityEngine;

public interface ISaveable
{
    void Save();
}

public static class SaveTools : ISaveable
{
    public static void Save()
    {
        Debug.Log("saved");
    }
}
""", """
using UnityEngine;

public interface ISaveable
{
    void Save();
}

public static class SaveTools
{
    public static void Save()
    {
        Debug.Log("saved");
    }
}
""", 8)

# 236 CS0718 — static 타입을 제네릭 인자로 넣었다.
ep('CS0718', 'Game.cs',
   "'SaveTools': static types cannot be used as type arguments", """
using System.Collections.Generic;
using UnityEngine;

public static class SaveTools
{
    public static string path = "save";
}

public class Game : MonoBehaviour
{
    List<SaveTools> log = new();

    void Start()
    {
        Debug.Log(log.Count);
    }
}
""", """
using System.Collections.Generic;
using UnityEngine;

public static class SaveTools
{
    public static string path = "save";
}

public class Game : MonoBehaviour
{
    List<string> log = new();

    void Start()
    {
        Debug.Log(log.Count);
    }
}
""", 11)

# 237 CS0721 — static 타입을 매개변수로 받았다.
ep('CS0721', 'Game.cs',
   "'SaveTools': static types cannot be used as parameters", """
using UnityEngine;

public static class SaveTools
{
    public static string path = "save";
}

public class Game : MonoBehaviour
{
    void Use(SaveTools tools)
    {
        Debug.Log("using");
    }
}
""", """
using UnityEngine;

public static class SaveTools
{
    public static string path = "save";
}

public class Game : MonoBehaviour
{
    void Use(string tools)
    {
        Debug.Log("using");
    }
}
""", 10)

# 238 CS0722 — static 타입을 반환형으로 썼다.
ep('CS0722', 'Game.cs',
   "'SaveTools': static types cannot be used as return types", """
using UnityEngine;

public static class SaveTools
{
    public static string path = "save";
}

public class Game : MonoBehaviour
{
    SaveTools Make()
    {
        return null;
    }
}
""", """
using UnityEngine;

public static class SaveTools
{
    public static string path = "save";
}

public class Game : MonoBehaviour
{
    string Make()
    {
        return null;
    }
}
""", 10)

# 239 CS0723 — static 타입으로 변수를 선언했다.
ep('CS0723', 'Game.cs',
   "Cannot declare a variable of static type 'SaveTools'", """
using UnityEngine;

public static class SaveTools
{
    public static void Save() { }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        SaveTools tools = null;
        SaveTools.Save();
    }
}
""", """
using UnityEngine;

public static class SaveTools
{
    public static void Save() { }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log("ready");
        SaveTools.Save();
    }
}
""", 12)

# 240 CS0441 — static 과 sealed 를 같이 붙였다.
ep('CS0441', 'SaveTools.cs',
   "'SaveTools': a class cannot be both static and sealed", """
using UnityEngine;

public static sealed class SaveTools
{
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
    public static string path = "save";

    public static void Save()
    {
        Debug.Log(path);
    }
}
""", 3)

# 241 CS1057 — static 클래스에 protected 멤버를 뒀다.
ep('CS1057', 'SaveTools.cs',
   "'SaveTools.slot': static classes cannot contain protected members", """
using UnityEngine;

public static class SaveTools
{
    protected static int slot;
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
    static int slot;
    public static string path = "save";

    public static void Save()
    {
        Debug.Log(path);
    }
}
""", 5)

# 242 CS0666 — 구조체에 protected 멤버를 뒀다.
ep('CS0666', 'Bag.cs',
   "'Slot.id': new protected member declared in struct", """
using UnityEngine;

public struct Slot
{
    protected int id;
    public int count;

    public int Id => id;
}

public class Bag : MonoBehaviour
{
    void Start()
    {
        Debug.Log(new Slot().Id);
    }
}
""", """
using UnityEngine;

public struct Slot
{
    int id;
    public int count;

    public int Id => id;
}

public class Bag : MonoBehaviour
{
    void Start()
    {
        Debug.Log(new Slot().Id);
    }
}
""", 5)

# 243 CS0065 — add 만 쓰고 remove 를 안 썼다.
ep('CS0065', 'Unit.cs',
   "'Unit.Died': event property must have both add and remove accessors", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    Action died;

    public event Action Died
    {
        add { died += value; }

    }

    void Die()
    {
        died?.Invoke();
    }
}
""", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    Action died;

    public event Action Died
    {
        add { died += value; }
        remove { died -= value; }
    }

    void Die()
    {
        died?.Invoke();
    }
}
""", 11)

# 244 CS0066 — 이벤트 타입을 델리게이트가 아닌 걸로 적었다.
ep('CS0066', 'Unit.cs', "'Unit.Died': event must be of a delegate type", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    public event int Died;
    public int hp = 100;

    void Die()
    {
        Died?.Invoke();
    }
}
""", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    public event Action Died;
    public int hp = 100;

    void Die()
    {
        Died?.Invoke();
    }
}
""", 6)

# 245 CS0070 — 이벤트에 = 로 대입했다.
ep('CS0070', 'Watcher.cs',
   "The event 'Unit.Died' can only appear on the left hand side of += or -=", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    public event Action Died;
}

public class Watcher : MonoBehaviour
{
    public Unit target;

    void Show() { }

    void Start()
    {
        target.Died = Show;
    }
}
""", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    public event Action Died;
}

public class Watcher : MonoBehaviour
{
    public Unit target;

    void Show() { }

    void Start()
    {
        target.Died += Show;
    }
}
""", 17)

# 246 CS0079 — 파생 클래스에서 이벤트에 = 로 대입했다.
ep('CS0079', 'Boss.cs',
   "The event 'Unit.Died' can only appear on the left hand side of += or -=", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    public event Action Died;
}

public class Boss : Unit
{
    void Show() { }

    void Start()
    {
        Died = Show;
    }
}
""", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    public event Action Died;
}

public class Boss : Unit
{
    void Show() { }

    void Start()
    {
        Died += Show;
    }
}
""", 15)

# 247 CS0073 — add 접근자에 본문을 안 썼다.
ep('CS0073', 'Unit.cs', "An add or remove accessor must have a body", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    Action died;

    public event Action Died
    {
        add;
        remove { died -= value; }
    }

    void Die()
    {
        died?.Invoke();
    }
}
""", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    Action died;

    public event Action Died
    {
        add { died += value; }
        remove { died -= value; }
    }

    void Die()
    {
        died?.Invoke();
    }
}
""", 10)

# 248 CS0123 — 델리게이트와 매개변수 개수가 다르다.
ep('CS0123', 'Watcher.cs',
   "No overload for 'Show' matches delegate 'Action'", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    void Show(int amount) { }

    void Start()
    {
        Action onHit = Show;
        onHit();
    }
}
""", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    void Show() { }

    void Start()
    {
        Action onHit = Show;
        onHit();
    }
}
""", 6)

# 249 CS0407 — 값을 돌려주는 메서드를 Action 에 넣었다.
ep('CS0407', 'Watcher.cs',
   "'int Watcher.GetScore()' has the wrong return type for delegate 'Action'", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    int GetScore() => 1;

    void Start()
    {
        Action show = GetScore;
        show();
    }
}
""", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    int GetScore() => 1;

    void Start()
    {
        Func<int> show = GetScore;
        show();
    }
}
""", 10)

# 250 CS1593 — 인자 없는 델리게이트에 인자 받는 람다를 넣었다.
ep('CS1593', 'Watcher.cs', "Delegate 'Action' does not take 1 arguments", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    Action onHit;

    void Start()
    {
        onHit = amount => Debug.Log(1);
        onHit();
    }
}
""", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    Action onHit;

    void Start()
    {
        onHit = () => Debug.Log(1);
        onHit();
    }
}
""", 10)

# 251 CS0574 — 클래스 이름을 바꾸고 소멸자를 안 고쳤다.
ep('CS0574', 'Player.cs', "Name of destructor must match name of class", """
using UnityEngine;

public class Player
{
    public int hp = 100;

    ~Enemy()
    {
        Debug.Log("gone");
    }
}
""", """
using UnityEngine;

public class Player
{
    public int hp = 100;

    ~Player()
    {
        Debug.Log("gone");
    }
}
""", 7)

# 252 CS0575 — 구조체에 소멸자를 뒀다.
ep('CS0575', 'Slot.cs', "Only class types can contain destructors", """
using UnityEngine;

public struct Slot
{
    public int id;

    ~Slot()
    {
        Debug.Log("gone");
    }
}
""", """
using UnityEngine;

public class Slot
{
    public int id;

    ~Slot()
    {
        Debug.Log("gone");
    }
}
""", 3)

# 253 CS0249 — Finalize 를 직접 override 했다.
ep('CS0249', 'Player.cs',
   "Do not override object.Finalize; provide a destructor instead", """
using UnityEngine;

public class Player
{
    public int hp = 100;

    protected override void Finalize()
    {
        Debug.Log("gone");
    }
}
""", """
using UnityEngine;

public class Player
{
    public int hp = 100;

    ~Player()
    {
        Debug.Log("gone");
    }
}
""", 7)

# 254 CS0245 — Finalize 를 직접 불렀다.
ep('CS0245', 'Game.cs',
   "Destructors and object.Finalize cannot be called directly", """
using UnityEngine;

public class Player
{
    ~Player()
    {
        Debug.Log("gone");
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Player hero = new Player();
        hero.Finalize();
    }
}
""", """
using UnityEngine;

public class Player
{
    ~Player()
    {
        Debug.Log("gone");
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Player hero = new Player();
        hero = null;
    }
}
""", 16)

# 255 CS0260 — 나눠 쓴 클래스 한쪽에 partial 을 안 붙였다.
ep('CS0260', 'Player.cs',
   "Missing partial modifier on declaration of type 'Player'", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;
}

public class Player
{
    public int mana = 50;
}
""", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;
}

public partial class Player
{
    public int mana = 50;
}
""", 8)

# 256 CS0261 — 한쪽을 struct 로 적었다.
ep('CS0261', 'Player.cs',
   "Partial declarations of 'Player' must be all classes or all structs", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;
}

public partial struct Player
{
    public int mana;
}
""", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;
}

public partial class Player
{
    public int mana;
}
""", 8)

# 257 CS0262 — 두 쪽의 접근 수준이 다르다.
ep('CS0262', 'Player.cs',
   "Partial declarations of 'Player' have conflicting accessibility modifiers", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;
}

internal partial class Player
{
    public int mana = 50;
}
""", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;
}

public partial class Player
{
    public int mana = 50;
}
""", 8)

# 258 CS0263 — 두 쪽이 서로 다른 기반 클래스를 적었다.
ep('CS0263', 'Boss.cs',
   "Partial declarations of 'Boss' must not specify different base classes", """
using UnityEngine;

public class Enemy { }
public class Unit { }

public partial class Boss : Enemy
{
    public int hp = 100;
}

public partial class Boss : Unit
{
    public int shield = 50;
}
""", """
using UnityEngine;

public class Enemy { }
public class Unit { }

public partial class Boss : Enemy
{
    public int hp = 100;
}

public partial class Boss
{
    public int shield = 50;
}
""", 11)

# 259 CS0264 — 두 쪽의 타입 매개변수 이름이 다르다.
ep('CS0264', 'Box.cs',
   "Partial declarations of 'Box<T>' must have the same type parameter names", """
using UnityEngine;

public partial class Box<T>
{
    public T value;
}

public partial class Box<U>
{
    public int count;
}

public class Crate : MonoBehaviour
{
    Box<int> box = new Box<int>();
}
""", """
using UnityEngine;

public partial class Box<T>
{
    public T value;
}

public partial class Box<T>
{
    public int count;
}

public class Crate : MonoBehaviour
{
    Box<int> box = new Box<int>();
}
""", 8)

# 260 CS0267 — partial 을 static 앞에 뒀다.
ep('CS0267', 'SaveTools.cs',
   "The partial modifier can only appear immediately before class, struct or interface", """
using UnityEngine;

partial static class SaveTools
{
    public static string path = "save";

    public static void Save()
    {
        Debug.Log(path);
    }
}
""", """
using UnityEngine;

static partial class SaveTools
{
    public static string path = "save";

    public static void Save()
    {
        Debug.Log(path);
    }
}
""", 3)

# 261 CS0751 — partial 메서드를 일반 클래스에 뒀다.
ep('CS0751', 'Player.cs',
   "A partial method must be declared within a partial class or partial struct", """
using UnityEngine;

public class Player
{
    public int hp = 100;

    partial void OnHit();

    void Show()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;

    partial void OnHit();

    void Show()
    {
        Debug.Log(hp);
    }
}
""", 3)

# 262 CS0759 — 선언 없이 본문만 썼다.
ep('CS0759', 'Player.cs',
   "No defining declaration found for implementing declaration of 'Player.OnHit()'", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;

    partial void OnHit() { }

    void Show()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;

    partial void OnHit();

    void Show()
    {
        Debug.Log(hp);
    }
}
""", 7)

# 263 CS0756 — 같은 partial 메서드를 두 번 선언했다.
ep('CS0756', 'Player.cs',
   "A partial method may not have multiple defining declarations", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;

    partial void OnHit();
    partial void OnHit();

    void Show()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public partial class Player
{
    public int hp = 100;

    partial void OnHit();
    partial void OnDie();

    void Show()
    {
        Debug.Log(hp);
    }
}
""", 8)

# 264 CS0757 — 같은 partial 메서드에 본문을 두 번 썼다.
ep('CS0757', 'Player.cs',
   "A partial method may not have multiple implementing declarations", """
using UnityEngine;

public partial class Player
{
    partial void OnHit();
    partial void OnDie();

    partial void OnHit() { }
    partial void OnHit() { }

    void Show()
    {
        Debug.Log(1);
    }
}
""", """
using UnityEngine;

public partial class Player
{
    partial void OnHit();
    partial void OnDie();

    partial void OnHit() { }
    partial void OnDie() { }

    void Show()
    {
        Debug.Log(1);
    }
}
""", 9)

# 265 CS0104 — System 과 UnityEngine 에 같은 이름이 있다.
ep('CS0104', 'Spawner.cs',
   "'Random' is an ambiguous reference between 'System.Random' and 'UnityEngine.Random'", """
using System;
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public int total = 5;

    void Start()
    {
        var picker = new Random();
        Debug.Log(total);
    }
}
""", """
using System;
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public int total = 5;

    void Start()
    {
        var picker = new System.Random();
        Debug.Log(total);
    }
}
""", 10)

# 267 CS0229 — 두 인터페이스에 같은 이름의 멤버가 있다.
ep('CS0229', 'Readout.cs',
   "Ambiguity between 'IHit.Value' and 'IDef.Value'", """
using UnityEngine;

public interface IHit
{
    int Value { get; }
}
public interface IDef
{
    int Value { get; }
}
public interface IStat : IHit, IDef { }
public class Readout : MonoBehaviour
{
    public IStat stat;

    void Start()
    {
        Debug.Log(stat.Value);
    }
}
""", """
using UnityEngine;

public interface IHit
{
    int Value { get; }
}
public interface IDef
{
    int Value { get; }
}
public interface IStat : IHit, IDef { }
public class Readout : MonoBehaviour
{
    public IStat stat;

    void Start()
    {
        Debug.Log(((IHit)stat).Value);
    }
}
""", 18)

# 268 CS0121 — 어느 오버로드인지 정할 수 없다.
ep('CS0121', 'Combat.cs',
   "The call is ambiguous between 'Hit(int, float)' and 'Hit(float, int)'", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    void Hit(int power, float delay) { }
    void Hit(float power, int delay) { }

    void Start()
    {
        Hit(1, 1);
    }
}
""", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    void Hit(int power, float delay) { }
    void Hit(float power, int delay) { }

    void Start()
    {
        Hit(1, 1f);
    }
}
""", 10)

# 269 CS0118 — 변수 이름을 안 적고 타입에 대입했다.
ep('CS0118', 'Game.cs', "'Player' is a type but is used like a variable", """
using UnityEngine;

public class Player
{
    public int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Player = new Player();
        Debug.Log("spawned");
    }
}
""", """
using UnityEngine;

public class Player
{
    public int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        var hero = new Player();
        Debug.Log("spawned");
    }
}
""", 12)

# 270 CS0119 — 변수 대신 타입 이름을 넘겼다.
ep('CS0119', 'Game.cs',
   "'Player' is a type, which is not valid in the given context", """
using UnityEngine;

public class Player
{
    public int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Player hero = new Player();
        Debug.Log(Player);
    }
}
""", """
using UnityEngine;

public class Player
{
    public int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Player hero = new Player();
        Debug.Log(hero.hp);
    }
}
""", 13)

# 271 CS1955 — 필드를 메서드처럼 불렀다.
ep('CS1955', 'Game.cs',
   "Non-invocable member 'Player.hp' cannot be used like a method", """
using UnityEngine;

public class Player
{
    public int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Player hero = new Player();
        Debug.Log(hero.hp());
    }
}
""", """
using UnityEngine;

public class Player
{
    public int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Player hero = new Player();
        Debug.Log(hero.hp);
    }
}
""", 13)

# 272 CS0149 — 델리게이트에 메서드가 아닌 값을 넘겼다.
ep('CS0149', 'Watcher.cs', "Method name expected", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    void Show() { }

    void Start()
    {
        Action onHit = new Action(1);
        onHit();
    }
}
""", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    void Show() { }

    void Start()
    {
        Action onHit = new Action(Show);
        onHit();
    }
}
""", 10)

# 273 CS0462 — 제네릭을 치환하니 두 오버로드가 같아졌다.
ep('CS0462', 'Boss.cs',
   "The inherited members 'Unit<int>.Hit(int)' and 'Unit<int>.Hit(T)' have the same signature", """
using UnityEngine;

public class Unit<T>
{
    public virtual void Hit(T item) { }
    public virtual void Hit(int id) { }
}

public class Boss : Unit<int>
{
    public int hp = 100;
}
""", """
using UnityEngine;

public class Unit<T>
{
    public virtual void Hit(T item) { }
    public virtual void Die(int id) { }
}

public class Boss : Unit<int>
{
    public int hp = 100;
}
""", 6)

# 274 CS0663 — ref 와 out 만 다른 오버로드를 만들었다.
ep('CS0663', 'Player.cs',
   "'Player' cannot define an overload that differs only on ref, out and in", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public void Hit(ref int value) { }

    public void Hit(out int value)
    {
        value = 0;
    }

    void Start()
    {
        int hp = 1;
        Hit(ref hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public void Hit(ref int value) { }

    public void Heal(out int value)
    {
        value = 0;
    }

    void Start()
    {
        int hp = 1;
        Hit(ref hp);
    }
}
""", 7)

# 275 CS1540 — 형제 인스턴스의 protected 멤버를 읽었다.
ep('CS1540', 'Boss.cs',
   "Cannot access protected member 'Enemy.hp' through a qualifier of type 'Enemy'", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    protected int hp = 100;
}

public class Boss : Enemy
{
    void Copy(Enemy other)
    {
        Debug.Log(other.hp);
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    protected int hp = 100;
}

public class Boss : Enemy
{
    void Copy(Boss other)
    {
        Debug.Log(other.hp);
    }
}
""", 10)

# 276 CS0572 — 인스턴스를 통해 중첩 타입을 꺼내려 했다.
ep('CS0572', 'Game.cs',
   "'Inner': cannot reference a type through an expression", """
using UnityEngine;

public class Outer
{
    public class Inner
    {
        public int id;
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Outer outer = new Outer();
        var slot = new outer.Inner();
    }
}
""", """
using UnityEngine;

public class Outer
{
    public class Inner
    {
        public int id;
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Outer outer = new Outer();
        var slot = new Outer.Inner();
    }
}
""", 16)

if __name__ == '__main__':
    write(E, 'tier4c.json')
