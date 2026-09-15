# -*- coding: utf-8 -*-
"""8티어 경고와 unsafe·XML 문서 주석."""
from _common import make, write

E = {}
ep = make(E)

ep('CS0067', 'Unit.cs', "The event 'Unit.Died' is never used", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{
    event Action Died;
    public int hp = 100;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", """
using System;
using UnityEngine;

public class Unit : MonoBehaviour
{

    public int hp = 100;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 6)

ep('CS0164', 'Loader.cs', "This label has not been referenced", """
using UnityEngine;

public class Loader : MonoBehaviour
{
    public int tries = 0;

    void Start()
    {
retry:
        tries++;
        Debug.Log(tries);
    }
}
""", """
using UnityEngine;

public class Loader : MonoBehaviour
{
    public int tries = 0;

    void Start()
    {

        tries++;
        Debug.Log(tries);
    }
}
""", 9)

ep('CS0108', 'Boss.cs',
   "'Boss.hp' hides inherited member 'Enemy.hp'; use the new keyword if intended", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Enemy
{
    public int hp = 500;
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;
}

public class Boss : Enemy
{
    public new int hp = 500;
}
""", 10)

ep('CS0114', 'Boss.cs',
   "'Boss.Hit()' hides inherited member 'Enemy.Hit()'; add the override keyword", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public virtual void Hit() { }
}

public class Boss : Enemy
{
    public void Hit() { }
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
""", 10)

ep('CS0162', 'Health.cs', "Unreachable code detected", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Die()
    {
        Debug.Log("dead");
        return;
        hp = 0;
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Die()
    {
        Debug.Log("dead");
        return;

    }
}
""", 11)
ep('CS0252', 'SaveSlot.cs',
   "Possible unintended reference comparison; cast the left side to type 'string'", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        object raw = "1200";
        string saved = "1200";
        if (raw == saved)
        {
            Debug.Log("same");
        }
    }
}
""", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        object raw = "1200";
        string saved = "1200";
        if ((string)raw == saved)
        {
            Debug.Log("same");
        }
    }
}
""", 9)

ep('CS1717', 'Health.cs',
   "Assignment made to same variable; did you mean to assign something else?", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Reset(int hp)
    {
        hp = hp;
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Reset(int hp)
    {
        this.hp = hp;
        Debug.Log(hp);
    }
}
""", 9)

ep('CS1718', 'Health.cs',
   "Comparison made to same variable; did you mean to compare something else?", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;
    public int max = 100;

    void Start()
    {
        if (hp == hp)
        {
            Debug.Log("full");
        }
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;
    public int max = 100;

    void Start()
    {
        if (hp == max)
        {
            Debug.Log("full");
        }
    }
}
""", 10)

ep('CS0665', 'Health.cs',
   "Assignment in conditional expression is always constant; did you mean == ?", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public bool alive = false;

    void Start()
    {
        if (alive = true)
        {
            Debug.Log("alive");
        }
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public bool alive = false;

    void Start()
    {
        if (alive == true)
        {
            Debug.Log("alive");
        }
    }
}
""", 9)

ep('CS0642', 'Health.cs', "Possible mistaken empty statement", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        if (hp > 0);
            Debug.Log("alive");
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        if (hp > 0)
            Debug.Log("alive");
    }
}
""", 9)

ep('CS0251', 'Scores.cs', "Indexing an array with a negative index", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    int[] best = new int[3];

    void Start()
    {
        Debug.Log(best[-1]);
    }
}
""", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    int[] best = new int[3];

    void Start()
    {
        Debug.Log(best[0]);
    }
}
""", 9)

ep('CS0078', 'Wallet.cs',
   "The 'l' suffix is easily confused with the digit '1'; use 'L' instead", """
using UnityEngine;

public class Wallet : MonoBehaviour
{
    long gold = 10L;
    long gems = 20L;
    long dust = 30l;
    long ore = 40L;

    void Start()
    {
        Debug.Log(gold);
    }
}
""", """
using UnityEngine;

public class Wallet : MonoBehaviour
{
    long gold = 10L;
    long gems = 20L;
    long dust = 30L;
    long ore = 40L;

    void Start()
    {
        Debug.Log(gold);
    }
}
""", 7)

ep('CS0675', 'Flags.cs',
   "Bitwise-or operator used on a sign-extended operand", """
using UnityEngine;

public class Flags : MonoBehaviour
{
    void Start()
    {
        int mask = -1;
        long all = mask | 0x10000L;
        Debug.Log(all);
    }
}
""", """
using UnityEngine;

public class Flags : MonoBehaviour
{
    void Start()
    {
        int mask = -1;
        long all = (uint)mask | 0x10000L;
        Debug.Log(all);
    }
}
""", 8)

ep('CS0661', 'Tile.cs',
   "'Tile' defines operator == or != but does not override Object.GetHashCode()", """
using UnityEngine;

public struct Tile
{
    public static bool operator ==(
        Tile left, Tile right) => true;

    public static bool operator !=(
        Tile left, Tile right) => false;


}
""", """
using UnityEngine;

public struct Tile
{
    public static bool operator ==(
        Tile left, Tile right) => true;

    public static bool operator !=(
        Tile left, Tile right) => false;

    public override int GetHashCode() => 0;
}
""", 11)

ep('CS0628', 'Player.cs',
   "'Player.hp': new protected member declared in sealed type", """
using UnityEngine;

public sealed class Player
{
    protected int hp = 100;
    public int mana = 50;

    public void Log()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public sealed class Player
{
    int hp = 100;
    public int mana = 50;

    public void Log()
    {
        Debug.Log(hp);
    }
}
""", 5)

ep('CS0693', 'Box.cs',
   "Type parameter 'T' has the same name as the type parameter from outer type 'Box<T>'", """
using UnityEngine;

public class Box<T>
{
    public T item;

    public class Inner<T>
    {
        public int value;
    }
}
""", """
using UnityEngine;

public class Box<T>
{
    public T item;

    public class Inner<U>
    {
        public int value;
    }
}
""", 7)

ep('CS0420', 'Counter.cs',
   "'Counter.hits': a reference to a volatile field will not be treated as volatile", """
using System.Threading;
using UnityEngine;

public class Counter : MonoBehaviour
{
    volatile int hits;

    void Bump()
    {
        Interlocked.Increment(ref hits);
        Debug.Log(hits);
    }
}
""", """
using System.Threading;
using UnityEngine;

public class Counter : MonoBehaviour
{
    int hits;

    void Bump()
    {
        Interlocked.Increment(ref hits);
        Debug.Log(hits);
    }
}
""", 6)

ep('CS0282', 'Bag.cs',
   "There is no defined ordering between fields in multiple declarations of 'Slot'", """
using UnityEngine;

public partial struct Slot
{
    public int id;
}

public partial struct Slot
{
    public int count;
}

public class Bag : MonoBehaviour
{
    Slot slot;
}
""", """
using UnityEngine;

public partial struct Slot
{
    public int id;
}

public partial struct Slot
{

}

public class Bag : MonoBehaviour
{
    Slot slot;
}
""", 10)

ep('CS1066', 'Boss.cs',
   "The default value for 'amount' will have no effect in an interface implementation", """
using UnityEngine;

public interface IHit
{
    void Hit(int amount);
}

public class Boss : IHit
{
    public void Hit(int amount = 1)
    {
        Debug.Log(amount);
    }
}
""", """
using UnityEngine;

public interface IHit
{
    void Hit(int amount);
}

public class Boss : IHit
{
    public void Hit(int amount)
    {
        Debug.Log(amount);
    }
}
""", 10)

ep('CS0728', 'SaveFile.cs',
   "Possibly incorrect assignment to local 'data' which is the argument to a using", """
using System.IO;
using UnityEngine;

public class SaveFile : MonoBehaviour
{
    void Load()
    {
        var data = File.OpenRead("save");
        using (data)
        {
            data = null;
        }
    }
}
""", """
using System.IO;
using UnityEngine;

public class SaveFile : MonoBehaviour
{
    void Load()
    {
        var data = File.OpenRead("save");
        using (data)
        {
            Debug.Log(data);
        }
    }
}
""", 11)

ep('CS1591', 'Score.cs',
   "Missing XML comment for publicly visible type or member 'Score.value'", """
using UnityEngine;

/// <summary>Holds the score.</summary>
public class Score : MonoBehaviour
{

    public int value;

    /// <summary>Resets it.</summary>
    public void ResetScore()
    {
        value = 0;
    }
}
""", """
using UnityEngine;

/// <summary>Holds the score.</summary>
public class Score : MonoBehaviour
{
    /// <summary>The score.</summary>
    public int value;

    /// <summary>Resets it.</summary>
    public void ResetScore()
    {
        value = 0;
    }
}
""", 6)

ep('CS1570', 'Score.cs', "XML comment has badly formed XML", """
using UnityEngine;

/// <summary>Holds the score.</summary
public class Score : MonoBehaviour
{
    public int value;

    public void ResetScore()
    {
        value = 0;
    }
}
""", """
using UnityEngine;

/// <summary>Holds the score.</summary>
public class Score : MonoBehaviour
{
    public int value;

    public void ResetScore()
    {
        value = 0;
    }
}
""", 3)

ep('CS1571', 'Stats.cs',
   "XML comment has a duplicate param tag for 'hp'", """
using UnityEngine;

public class Stats : MonoBehaviour
{
    /// <param name="hp">Health.</param>
    /// <param name="hp">Mana.</param>
    public void Set(int hp, int mana)
    {
        Debug.Log(hp + mana);
    }
}
""", """
using UnityEngine;

public class Stats : MonoBehaviour
{
    /// <param name="hp">Health.</param>
    /// <param name="mana">Mana.</param>
    public void Set(int hp, int mana)
    {
        Debug.Log(hp + mana);
    }
}
""", 6)

ep('CS1572', 'Stats.cs',
   "XML comment has a param tag for 'mana', but there is no parameter by that name", """
using UnityEngine;

public class Stats : MonoBehaviour
{
    /// <summary>Sets health.</summary>
    /// <param name="mana">Mana.</param>
    public void SetHp(int hp)
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public class Stats : MonoBehaviour
{
    /// <summary>Sets health.</summary>
    /// <param name="hp">Health.</param>
    public void SetHp(int hp)
    {
        Debug.Log(hp);
    }
}
""", 6)

ep('CS1573', 'Stats.cs',
   "Parameter 'mana' has no matching param tag in the XML comment", """
using UnityEngine;

public class Stats : MonoBehaviour
{
    /// <param name="hp">Health.</param>

    public void Set(int hp, int mana)
    {
        Debug.Log(hp + mana);
    }
}
""", """
using UnityEngine;

public class Stats : MonoBehaviour
{
    /// <param name="hp">Health.</param>
    /// <param name="mana">Mana.</param>
    public void Set(int hp, int mana)
    {
        Debug.Log(hp + mana);
    }
}
""", 6)

ep('CS1574', 'Combat.cs',
   "XML comment has cref attribute 'Heal' that could not be resolved", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    /// <summary>Hits once.</summary>
    /// <see cref="Heal"/>
    public void Attack()
    {
        Debug.Log("attack");
    }
}
""", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    /// <summary>Hits once.</summary>
    /// <see cref="Attack"/>
    public void Attack()
    {
        Debug.Log("attack");
    }
}
""", 6)

ep('CS1587', 'Combat.cs',
   "XML comment is not placed on a valid language element", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    public void Attack()
    {
        /// <summary>Damage.</summary>
        int damage = 10;
        Debug.Log(damage);
    }
}
""", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    public void Attack()
    {
        // Base damage.
        int damage = 10;
        Debug.Log(damage);
    }
}
""", 7)

ep('CS0465', 'Player.cs',
   "Introducing a Finalize method can interfere with destructor invocation", """
using UnityEngine;

public class Player
{
    public int hp = 100;

    protected virtual void Finalize()
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

ep('CS0658', 'Player.cs',
   "'x' is not a recognized attribute location; use 'method' or 'return'", """
using System;
using UnityEngine;

public class Player : MonoBehaviour
{
    [x: Obsolete]
    public void Hit()
    {
        Debug.Log("hit");
    }
}
""", """
using System;
using UnityEngine;

public class Player : MonoBehaviour
{
    [Obsolete]
    public void Hit()
    {
        Debug.Log("hit");
    }
}
""", 6)

ep('CS1981', 'SaveSlot.cs',
   "Using 'is' to test compatibility with 'dynamic' is identical to testing 'object'", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        object raw = 1;
        if (raw is dynamic)
        {
            Debug.Log(raw);
        }
    }
}
""", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        object raw = 1;
        if (raw is int)
        {
            Debug.Log(raw);
        }
    }
}
""", 8)

ep('CS0208', 'Pixels.cs',
   "Cannot declare a pointer to the managed type 'Player'", """
using UnityEngine;

public class Player
{
    public int hp;
}

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        Player* raw = null;
        Debug.Log(1);
    }
}
""", """
using UnityEngine;

public class Player
{
    public int hp;
}

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int* raw = null;
        Debug.Log(1);
    }
}
""", 12)

ep('CS0214', 'Pixels.cs',
   "Pointers and fixed size buffers may only be used in an unsafe context", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    void Scan()
    {
        int count = 1;
        int* raw = &count;
        Debug.Log(1);
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int count = 1;
        int* raw = &count;
        Debug.Log(1);
    }
}
""", 5)

ep('CS0227', 'Pixels.cs',
   "Unsafe code may only appear if compiling with the unsafe option", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int count = 1;
        Debug.Log(count);
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    void Scan()
    {
        int count = 1;
        Debug.Log(count);
    }
}
""", 5)

ep('CS0209', 'Pixels.cs',
   "The type of a local declared in a fixed statement must be a pointer type", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    int[] data = new int[3];

    unsafe void Scan()
    {
        fixed (int head = data)
        {
            Debug.Log(1);
        }
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    int[] data = new int[3];

    unsafe void Scan()
    {
        fixed (int* head = data)
        {
            Debug.Log(1);
        }
    }
}
""", 9)

ep('CS0211', 'Pixels.cs',
   "Cannot take the address of the given expression", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int count = 1;
        int* raw = &(count + 1);
        Debug.Log(1);
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int count = 1;
        int* raw = &count;
        Debug.Log(1);
    }
}
""", 8)

ep('CS0213', 'Pixels.cs',
   "You cannot use the fixed statement to take the address of an already fixed expression", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int count = 1;
        fixed (int* raw = &count)
        {
            Debug.Log(1);
        }
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int count = 1;
        int* raw = &count;
        {
            Debug.Log(1);
        }
    }
}
""", 8)

ep('CS0193', 'Pixels.cs',
   "The * or -> operator must be applied to a pointer", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int count = 1;
        Debug.Log(*count);
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        int count = 1;
        Debug.Log(count);
    }
}
""", 8)

ep('CS0196', 'Pixels.cs',
   "A pointer must be indexed by only one value", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    public int width = 4;

    unsafe void Scan(int* data)
    {
        Debug.Log(data[0, 1]);
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    public int width = 4;

    unsafe void Scan(int* data)
    {
        Debug.Log(data[0]);
    }
}
""", 9)

ep('CS0242', 'Pixels.cs',
   "The operation in question is undefined on void pointers", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    public int width = 4;

    unsafe void Scan(void* data)
    {
        data = data + 1;
        Debug.Log(width);
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    public int width = 4;

    unsafe void Scan(void* data)
    {
        data = (byte*)data + 1;
        Debug.Log(width);
    }
}
""", 9)

ep('CS0244', 'Pixels.cs',
   "Neither 'is' nor 'as' is valid on pointer types", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    public int width = 4;

    unsafe void Scan(int* data)
    {
        if (data is object)
        {
            Debug.Log(width);
        }
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    public int width = 4;

    unsafe void Scan(int* data)
    {
        if (data != null)
        {
            Debug.Log(width);
        }
    }
}
""", 9)

ep('CS0247', 'Pixels.cs',
   "Cannot use a negative size with stackalloc", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    public int width = 4;

    unsafe void Scan()
    {
        int* buffer = stackalloc int[-1];
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

ep('CS0248', 'Scores.cs',
   "Cannot create an array with a negative size", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    public int count = 3;

    void Start()
    {
        int[] best = new int[-1];
        Debug.Log(best.Length);
    }
}
""", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    public int count = 3;

    void Start()
    {
        int[] best = new int[count];
        Debug.Log(best.Length);
    }
}
""", 9)

if __name__ == '__main__':
    write(E, 'tier8.json')
