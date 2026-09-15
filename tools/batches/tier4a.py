# -*- coding: utf-8 -*-
"""4티어 앞부분: 구조체 반환값·접근 수준·override·abstract·인터페이스."""
from _common import make, write

E = {}
ep = make(E)

# 153 CS0198 — static readonly 필드를 나중에 바꾸려 했다.
ep('CS0198', 'Player.cs',
   "A static readonly field cannot be assigned to outside a static constructor", """
using UnityEngine;

public class Player : MonoBehaviour
{
    static readonly int maxHp = 100;

    public void Rebalance()
    {
        maxHp = 50;
        Debug.Log(maxHp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    static int maxHp = 100;

    public void Rebalance()
    {
        maxHp = 50;
        Debug.Log(maxHp);
    }
}
""", 5)

# 154 CS1612 — transform.position 의 한 축만 바꾸려 했다.
ep('CS1612', 'Turret.cs',
   "Cannot modify the return value of 'Transform.position'", """
using UnityEngine;

public class Turret : MonoBehaviour
{
    public float range = 5f;

    void Aim()
    {
        transform.position.x = 5f;
        Debug.Log(transform.position);
    }
}
""", """
using UnityEngine;

public class Turret : MonoBehaviour
{
    public float range = 5f;

    void Aim()
    {
        transform.Translate(5f, 0, 0);
        Debug.Log(transform.position);
    }
}
""", 9)

# 155 CS1648 — readonly 구조체 필드의 한 축만 바꾸려 했다.
ep('CS1648', 'Turret.cs',
   "Members of readonly field 'Turret.origin' cannot be modified", """
using UnityEngine;

public class Turret : MonoBehaviour
{
    readonly Vector3 origin;

    void ResetAim()
    {
        origin.x = 5f;
        Debug.Log(origin);
    }
}
""", """
using UnityEngine;

public class Turret : MonoBehaviour
{
    Vector3 origin;

    void ResetAim()
    {
        origin.x = 5f;
        Debug.Log(origin);
    }
}
""", 5)

# 156 CS0445 — 박싱된 값을 캐스트해서 바로 고치려 했다.
ep('CS0445', 'SaveSlot.cs',
   "Cannot modify the result of an unboxing conversion", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    object boxed = new Vector3();

    void Start()
    {
        ((Vector3)boxed).x = 1f;
        Debug.Log(boxed);
    }
}
""", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    object boxed = new Vector3();

    void Start()
    {
        boxed = new Vector3(1f, 0, 0);
        Debug.Log(boxed);
    }
}
""", 9)

# 157 CS0428 — 메서드를 부르지 않고 이름만 대입했다.
ep('CS0428', 'Combat.cs',
   "Cannot convert method group 'Damage' to non-delegate type 'int'", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int Damage() => 10;
}

public class Combat : MonoBehaviour
{
    public Enemy target;

    void Start()
    {
        int hit = target.Damage;
        Debug.Log(hit);
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int Damage() => 10;
}

public class Combat : MonoBehaviour
{
    public Enemy target;

    void Start()
    {
        int hit = target.Damage();
        Debug.Log(hit);
    }
}
""", 14)

# 158 CS0269 — out 매개변수를 채우기 전에 읽었다.
ep('CS0269', 'Inventory.cs',
   "Use of unassigned out parameter 'count'", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    public bool TryTake(out int count)
    {
        Debug.Log("Taking " + count);
        count = 1;
        return true;
    }

    void Start()
    {
        TryTake(out int taken);
    }
}
""", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    public bool TryTake(out int count)
    {
        Debug.Log("Taking one");
        count = 1;
        return true;
    }

    void Start()
    {
        TryTake(out int taken);
    }
}
""", 7)

# 159 CS0177 — 빠져나가는 경로에서 out 을 안 채웠다.
ep('CS0177', 'Inventory.cs',
   "The out parameter 'count' must be assigned before control leaves the method", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    public bool TryTake(out int count)
    {
        Debug.Log("Taking");

        return false;
    }

    void Start()
    {
        TryTake(out int taken);
    }
}
""", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    public bool TryTake(out int count)
    {
        Debug.Log("Taking");
        count = 0;
        return false;
    }

    void Start()
    {
        TryTake(out int taken);
    }
}
""", 8)

# 160 CS0170 — 구조체를 선언만 하고 필드를 읽었다.
ep('CS0170', 'Bag.cs', "Use of possibly unassigned field 'id'", """
using UnityEngine;

public struct Slot
{
    public int id;
}

public class Bag : MonoBehaviour
{
    void Start()
    {
        Slot first;
        Debug.Log(first.id);
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
    void Start()
    {
        Slot first = default;
        Debug.Log(first.id);
    }
}
""", 12)

# 161 CS0050 — 도우미 클래스에 public 을 안 붙였다.
ep('CS0050', 'Bag.cs',
   "Inconsistent accessibility: return type 'Item' is less accessible than method 'Bag.Take()'", """
using UnityEngine;

class Item
{
    public int id;
}

public class Bag : MonoBehaviour
{
    public Item Take()
    {
        return null;
    }
}
""", """
using UnityEngine;

public class Item
{
    public int id;
}

public class Bag : MonoBehaviour
{
    public Item Take()
    {
        return null;
    }
}
""", 3)

# 162 CS0051 — 매개변수 타입이 메서드보다 좁다.
ep('CS0051', 'Bag.cs',
   "Inconsistent accessibility: parameter type 'Item' is less accessible than method", """
using UnityEngine;

class Item
{
    public int id;
}

public class Bag : MonoBehaviour
{
    public void Put(Item item)
    {
        Debug.Log(item.id);
    }
}
""", """
using UnityEngine;

public class Item
{
    public int id;
}

public class Bag : MonoBehaviour
{
    public void Put(Item item)
    {
        Debug.Log(item.id);
    }
}
""", 3)

# 163 CS0052 — 필드 타입이 필드보다 좁다.
ep('CS0052', 'Bag.cs',
   "Inconsistent accessibility: field type 'Item' is less accessible than field 'Bag.slot'", """
using UnityEngine;

class Item
{
    public int id;
}

public class Bag : MonoBehaviour
{
    public Item slot;

    void Start()
    {
        Debug.Log(slot);
    }
}
""", """
using UnityEngine;

public class Item
{
    public int id;
}

public class Bag : MonoBehaviour
{
    public Item slot;

    void Start()
    {
        Debug.Log(slot);
    }
}
""", 3)

# 164 CS0053 — 속성 타입이 속성보다 좁다.
ep('CS0053', 'Bag.cs',
   "Inconsistent accessibility: property type 'Item' is less accessible than property", """
using UnityEngine;

class Item
{
    public int id;
}

public class Bag : MonoBehaviour
{
    public Item Slot { get; set; }

    void Start()
    {
        Debug.Log(Slot);
    }
}
""", """
using UnityEngine;

public class Item
{
    public int id;
}

public class Bag : MonoBehaviour
{
    public Item Slot { get; set; }

    void Start()
    {
        Debug.Log(Slot);
    }
}
""", 3)

# 165 CS0060 — 기반 클래스가 파생 클래스보다 좁다.
ep('CS0060', 'Boss.cs',
   "Inconsistent accessibility: base class 'Enemy' is less accessible than class 'Boss'", """
using UnityEngine;

class Enemy : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Enemy
{
    public int shield = 50;
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Enemy
{
    public int shield = 50;
}
""", 3)

# 166 CS0061 — 기반 인터페이스가 더 좁다.
ep('CS0061', 'Breakable.cs',
   "Inconsistent accessibility: base interface 'IDamage' is less accessible than interface", """
interface IDamage
{
    void TakeHit(int amount);
}

public interface IBreak : IDamage
{
    void Shatter();
}

public class Crate { }
""", """
public interface IDamage
{
    void TakeHit(int amount);
}

public interface IBreak : IDamage
{
    void Shatter();
}

public class Crate { }
""", 1)

# 167 CS0112 — static 메서드에 virtual 을 붙였다.
ep('CS0112', 'Enemy.cs',
   "A static member cannot be marked as override, virtual or abstract", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    public static virtual void Reset()
    {
        Debug.Log("reset");
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    public static void Reset()
    {
        Debug.Log("reset");
    }
}
""", 7)

# 168 CS0113 — override 에 virtual 을 같이 붙였다.
ep('CS0113', 'Boss.cs',
   "A member marked as override cannot be marked as new or virtual", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public virtual void Hit()
    {
        Debug.Log("hit");
    }
}

public class Boss : Enemy
{
    public override virtual void Hit()
    {
        Debug.Log("boss hit");
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public virtual void Hit()
    {
        Debug.Log("hit");
    }
}

public class Boss : Enemy
{
    public override void Hit()
    {
        Debug.Log("boss hit");
    }
}
""", 13)

# 169 CS0115 — 부모에 없는 이름을 override 했다.
ep('CS0115', 'Boss.cs',
   "'Boss.Heal()' no suitable method found to override", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public virtual void Attack()
    {
        Debug.Log("attack");
    }
}

public class Boss : Enemy
{
    public override void Heal()
    {
        Debug.Log("heal");
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public virtual void Attack()
    {
        Debug.Log("attack");
    }
}

public class Boss : Enemy
{
    public override void Attack()
    {
        Debug.Log("heal");
    }
}
""", 13)

# 170 CS0506 — 부모에 virtual 을 안 붙였다.
ep('CS0506', 'Boss.cs',
   "'Boss.Damage()' cannot override inherited member 'Enemy.Damage()'; it is not virtual", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int Damage()
    {
        return 10;
    }
}

public class Boss : Enemy
{
    public override int Damage()
    {
        return 50;
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public virtual int Damage()
    {
        return 10;
    }
}

public class Boss : Enemy
{
    public override int Damage()
    {
        return 50;
    }
}
""", 5)

# 171 CS0507 — override 하면서 접근 수준을 올렸다.
ep('CS0507', 'Boss.cs',
   "'Boss.Hit()' cannot change access modifiers when overriding inherited member", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    protected virtual void Hit()
    {
        Debug.Log("hit");
    }
}

public class Boss : Enemy
{
    public override void Hit()
    {
        Debug.Log("boss hit");
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    protected virtual void Hit()
    {
        Debug.Log("hit");
    }
}

public class Boss : Enemy
{
    protected override void Hit()
    {
        Debug.Log("boss hit");
    }
}
""", 13)

# 172 CS0508 — override 에서 반환형을 바꿨다.
ep('CS0508', 'Boss.cs',
   "'Boss.IsAlive()' return type must be 'bool' to match overridden member", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public virtual bool IsAlive()
    {
        return true;
    }
}

public class Boss : Enemy
{
    public override int IsAlive()
    {
        return default;
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public virtual bool IsAlive()
    {
        return true;
    }
}

public class Boss : Enemy
{
    public override bool IsAlive()
    {
        return default;
    }
}
""", 13)

# 173 CS0509 — sealed 클래스를 상속했다.
ep('CS0509', 'Boss.cs',
   "'Boss' cannot derive from sealed type 'Foe'", """
using UnityEngine;

public sealed class Foe : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Foe
{
    public int shield = 50;
}
""", """
using UnityEngine;

public class Foe : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Foe
{
    public int shield = 50;
}
""", 3)

# 174 CS0239 — sealed 로 막힌 멤버를 다시 override 했다.
ep('CS0239', 'King.cs',
   "'King.Hit()' cannot override inherited member because it is sealed", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public virtual void Hit() { }
}

public class Boss : Enemy
{
    public sealed override void Hit() { }
}

public class King : Boss
{
    public override void Hit() { }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public virtual void Hit() { }
}

public class Boss : Enemy
{
    public override void Hit() { }
}

public class King : Boss
{
    public override void Hit() { }
}
""", 10)

# 175 CS0238 — override 가 아닌 멤버에 sealed 를 붙였다.
ep('CS0238', 'Enemy.cs',
   "'Enemy.Hit()' cannot be sealed because it is not an override", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    public sealed void Hit()
    {
        hp -= 10;
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    public void Hit()
    {
        hp -= 10;
    }
}
""", 7)

# 176 CS0500 — abstract 메서드에 본문을 썼다.
ep('CS0500', 'Enemy.cs',
   "'Enemy.Hit()' cannot declare a body because it is marked abstract", """
using UnityEngine;

public abstract class Enemy
{
    public int hp = 100;

    public abstract void Hit()
    {
        hp -= 10;
    }

    public void Log()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public abstract class Enemy
{
    public int hp = 100;

    public virtual void Hit()
    {
        hp -= 10;
    }

    public void Log()
    {
        Debug.Log(hp);
    }
}
""", 7)

# 177 CS0501 — 본문 없이 선언만 했다.
ep('CS0501', 'Enemy.cs',
   "'Enemy.Hit()' must declare a body because it is not marked abstract or extern", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    public void Hit();

    void Start()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    public void Hit() { }

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 7)

# 178 CS0502 — abstract 와 sealed 를 같이 붙였다.
ep('CS0502', 'Enemy.cs',
   "'Enemy.Hit()' cannot be both abstract and sealed", """
using UnityEngine;

public abstract class Enemy
{
    public int hp = 100;

    public abstract sealed void Hit();

    public void Log()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public abstract class Enemy
{
    public int hp = 100;

    public abstract void Hit();

    public void Log()
    {
        Debug.Log(hp);
    }
}
""", 7)

# 179 CS0503 — abstract 와 virtual 을 같이 붙였다.
ep('CS0503', 'Enemy.cs',
   "'Enemy.Hit()' cannot be both abstract and virtual", """
using UnityEngine;

public abstract class Enemy
{
    public int hp = 100;

    public abstract virtual void Hit();

    public void Log()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public abstract class Enemy
{
    public int hp = 100;

    public abstract void Hit();

    public void Log()
    {
        Debug.Log(hp);
    }
}
""", 7)

# 180 CS0513 — 클래스에 abstract 를 안 붙였다.
ep('CS0513', 'Enemy.cs',
   "'Enemy.Hit()' is abstract but it is contained in non-abstract type 'Enemy'", """
using UnityEngine;

public class Enemy
{
    public int hp = 100;

    public abstract void Hit();

    public void Log()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public abstract class Enemy
{
    public int hp = 100;

    public abstract void Hit();

    public void Log()
    {
        Debug.Log(hp);
    }
}
""", 3)

# 181 CS0533 — override 대신 new 를 붙였다.
ep('CS0533', 'Boss.cs',
   "'Boss.Hit()' hides inherited abstract member 'Enemy.Hit()'", """
using UnityEngine;

public abstract class Enemy
{
    public abstract void Hit();
}

public class Boss : Enemy
{
    public new void Hit()
    {
        Debug.Log("boss hit");
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
    public override void Hit()
    {
        Debug.Log("boss hit");
    }
}
""", 10)

# 182 CS0534 — 상속만 하고 abstract 멤버를 안 채웠다.
ep('CS0534', 'Boss.cs',
   "'Boss' does not implement inherited abstract member 'Enemy.Hit()'", """
using UnityEngine;

public abstract class Enemy
{
    public abstract void Hit();
}

public class Boss : Enemy
{
    public int shield = 50;

    void Log()
    {
        Debug.Log(shield);
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
    public int shield = 50;

    void Log()
    {
        Debug.Log(shield);
    }
    public override void Hit() { }
}
""", 16)

# 183 CS0535 — 인터페이스를 붙이고 멤버를 안 만들었다.
ep('CS0535', 'Crate.cs',
   "'Crate' does not implement interface member 'IDamage.TakeHit(int)'", """
using UnityEngine;

public interface IDamage
{
    void TakeHit(int amount);
}

public class Crate : IDamage
{
    public int hp = 20;

    public void Log()
    {
        Debug.Log(hp);
    }

}
""", """
using UnityEngine;

public interface IDamage
{
    void TakeHit(int amount);
}

public class Crate : IDamage
{
    public int hp = 20;

    public void Log()
    {
        Debug.Log(hp);
    }
    public void TakeHit(int amount) { }
}
""", 16)

# 184 CS0540 — 명시적 구현만 쓰고 인터페이스를 안 붙였다.
ep('CS0540', 'Crate.cs',
   "'Crate.IDamage.TakeHit(int)': containing type does not implement interface", """
using UnityEngine;

public interface IDamage
{
    void TakeHit(int amount);
}

public class Crate
{
    public int hp = 20;

    void IDamage.TakeHit(int amount)
    {
        hp -= amount;
    }
}
""", """
using UnityEngine;

public interface IDamage
{
    void TakeHit(int amount);
}

public class Crate : IDamage
{
    public int hp = 20;

    void IDamage.TakeHit(int amount)
    {
        hp -= amount;
    }
}
""", 8)

# 185 CS0277 — 구현 메서드에 public 을 안 붙였다.
ep('CS0277', 'Crate.cs',
   "'Crate' does not implement interface member 'IDamage.TakeHit(int)'; it is not public", """
using UnityEngine;

public interface IDamage
{
    void TakeHit(int amount);
}

public class Crate : IDamage
{
    public int hp = 20;

    void TakeHit(int amount)
    {
        hp -= amount;
    }
}
""", """
using UnityEngine;

public interface IDamage
{
    void TakeHit(int amount);
}

public class Crate : IDamage
{
    public int hp = 20;

    public void TakeHit(int amount)
    {
        hp -= amount;
    }
}
""", 12)

# 186 CS0538 — 인터페이스가 아닌 타입 이름으로 명시적 구현을 썼다.
ep('CS0538', 'Crate.cs',
   "'Damage' in explicit interface declaration is not an interface", """
using UnityEngine;

public class Damage
{
    public void TakeHit(int amount) { }
}

public class Crate
{
    public int hp = 20;

    void Damage.TakeHit(int amount)
    {
        hp -= amount;
    }
}
""", """
using UnityEngine;

public class Damage
{
    public void TakeHit(int amount) { }
}

public class Crate
{
    public int hp = 20;

    public void TakeHit(int amount)
    {
        hp -= amount;
    }
}
""", 12)

# 187 CS0539 — 인터페이스에 없는 이름을 명시적 구현했다.
ep('CS0539', 'Crate.cs',
   "'Crate.Jump()' in explicit interface declaration is not a member of interface", """
using UnityEngine;

public interface IMovable
{
    void Move();
}

public class Crate : IMovable
{
    public void Move() { }

    void IMovable.Jump()
    {
        Debug.Log("jump");
    }
}
""", """
using UnityEngine;

public interface IMovable
{
    void Move();
}

public class Crate : IMovable
{
    public void Move() { }

    void IMovable.Move()
    {
        Debug.Log("jump");
    }
}
""", 12)

# 188 CS0541 — 인터페이스 안에서 명시적 구현을 썼다.
ep('CS0541', 'Breakable.cs',
   "'IBreak.IHit.Hit(int)': explicit interface declaration can only be declared in a class", """
using UnityEngine;

public interface IHit
{
    void Hit(int amount);
}

public interface IBreak : IHit
{
    void IHit.Hit(int amount) { }
}

public class Crate : IBreak
{
    public void Hit(int amount) { }
}
""", """
using UnityEngine;

public interface IHit
{
    void Hit(int amount);
}

public interface IBreak : IHit
{
    void Shatter();
}

public class Crate : IBreak
{
    public void Hit(int amount) { }
}
""", 10)

# 189 CS0542 — 메서드 이름을 클래스 이름과 같게 지었다.
ep('CS0542', 'Player.cs',
   "'Player': member names cannot be the same as their enclosing type", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    public void Player()
    {
        hp = 100;
    }

    void Start()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    public void ResetHp()
    {
        hp = 100;
    }

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 7)

# 190 CS0144 — 추상 클래스를 직접 만들었다.
ep('CS0144', 'Wave.cs',
   "Cannot create an instance of the abstract type or interface 'Enemy'", """
using UnityEngine;

public abstract class Enemy
{
    public abstract void Hit();
}

public class Boss : Enemy
{
    public override void Hit() { }
}

public class Wave : MonoBehaviour
{
    void Start()
    {
        Enemy foe = new Enemy();
        foe.Hit();
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
    public override void Hit() { }
}

public class Wave : MonoBehaviour
{
    void Start()
    {
        Enemy foe = new Boss();
        foe.Hit();
    }
}
""", 17)

# 191 CS0143 — void 를 타입처럼 만들려 했다.
ep('CS0143', 'Probe.cs',
   "The type 'void' has no constructors defined", """
using System;
using UnityEngine;

public class Probe : MonoBehaviour
{
    public Type kind = typeof(void);

    void Start()
    {
        var made = new System.Void();
        Debug.Log(made);
    }
}
""", """
using System;
using UnityEngine;

public class Probe : MonoBehaviour
{
    public Type kind = typeof(void);

    void Start()
    {
        var made = new object();
        Debug.Log(made);
    }
}
""", 10)

# 192 CS0516 — 다른 생성자를 부르려다 자기를 불렀다.
ep('CS0516', 'Player.cs',
   "Constructor 'Player.Player()' cannot call itself", """
using UnityEngine;

public class Player
{
    public int hp;

    public Player() : this()
    {
        Debug.Log("default");
    }

    public Player(int startHp)
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
""", 7)

if __name__ == '__main__':
    write(E, 'tier4a.json')
