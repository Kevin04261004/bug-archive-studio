# -*- coding: utf-8 -*-
"""2티어 뒷부분과 3티어 앞부분: 배열·foreach·리터럴 변환."""
from _common import make, write

E = {}
ep = make(E)

# 76 CS0724 — 재시도 정리 블록에서 다시 던지려 했다.
ep('CS0724', 'Uploader.cs',
   "A throw statement with no arguments is not allowed in a nested finally clause", """
using System;
using UnityEngine;

public class Uploader : MonoBehaviour
{
    void Send()
    {
        try { Debug.Log("Sending"); }
        catch
        {
            try { Debug.Log("Retry"); }
            finally
            {
                throw;
            }
        }
    }
}
""", """
using System;
using UnityEngine;

public class Uploader : MonoBehaviour
{
    void Send()
    {
        try { Debug.Log("Sending"); }
        catch
        {
            try { Debug.Log("Retry"); }
            finally
            {
                Debug.Log("Gave up");
            }
        }
    }
}
""", 14)

# 77 CS0127 — 반환형을 void 로 바꾸고 return 을 안 고쳤다.
ep('CS0127', 'ScoreUI.cs',
   "Since this method returns void, return must not be followed by a value", """
using UnityEngine;

public class ScoreUI : MonoBehaviour
{
    int score = 120;

    void ShowScore()
    {
        Debug.Log("Score: " + score);
        return score;
    }

    void Start()
    {
        ShowScore();
    }
}
""", """
using UnityEngine;

public class ScoreUI : MonoBehaviour
{
    int score = 120;

    void ShowScore()
    {
        Debug.Log("Score: " + score);
        return;
    }

    void Start()
    {
        ShowScore();
    }
}
""", 10)

# 78 CS0126 — 값을 돌려줘야 하는데 빈 return 으로 빠져나갔다.
ep('CS0126', 'Rewards.cs',
   "An object of a type convertible to 'int' is required", """
using UnityEngine;

public class Rewards : MonoBehaviour
{
    public int Bonus(bool won)
    {
        if (!won)
        {
            return;
        }
        return 100;
    }
}
""", """
using UnityEngine;

public class Rewards : MonoBehaviour
{
    public int Bonus(bool won)
    {
        if (!won)
        {
            return 0;
        }
        return 100;
    }
}
""", 9)

# 79 CS0131 — 상수를 왼쪽에 쓰는 습관이 대입문으로 나왔다.
ep('CS0131', 'Health.cs',
   "The left-hand side of an assignment must be a variable, property or indexer", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    public void ResetHp()
    {
        100 = hp;
        Debug.Log("HP reset");
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    public void ResetHp()
    {
        hp = 100;
        Debug.Log("HP reset");
    }
}
""", 9)

# 80 CS1059 — 계산 결과를 그 자리에서 증가시키려 했다.
ep('CS1059', 'Combo.cs',
   "The operand of an increment or decrement operator must be a variable", """
using UnityEngine;

public class Combo : MonoBehaviour
{
    public int hits = 0;
    public int bonus = 1;

    public void Register()
    {
        (hits + bonus)++;
        Debug.Log("Combo: " + hits);
    }
}
""", """
using UnityEngine;

public class Combo : MonoBehaviour
{
    public int hits = 0;
    public int bonus = 1;

    public void Register()
    {
        hits += bonus;
        Debug.Log("Combo: " + hits);
    }
}
""", 10)

# 81 CS0230 — 파이썬처럼 타입 없이 foreach 를 썼다.
ep('CS0230', 'Patrol.cs',
   "Type and identifier are both required in a foreach statement", """
using UnityEngine;

public class Patrol : MonoBehaviour
{
    public Vector3[] path;

    void Start()
    {
        foreach (spot in path)
        {
            Debug.Log(spot);
        }
    }
}
""", """
using UnityEngine;

public class Patrol : MonoBehaviour
{
    public Vector3[] path;

    void Start()
    {
        foreach (Vector3 spot in path)
        {
            Debug.Log(spot);
        }
    }
}
""", 9)

# 82 CS1579 — 배열 대신 개수를 순회했다.
ep('CS1579', 'Spawner.cs',
   "foreach cannot operate on 'int' because it has no GetEnumerator", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public int count = 3;
    public GameObject[] enemies;

    void Start()
    {
        foreach (var foe in count)
        {
            Instantiate(foe);
        }
    }
}
""", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public int count = 3;
    public GameObject[] enemies;

    void Start()
    {
        foreach (var foe in enemies)
        {
            Instantiate(foe);
        }
    }
}
""", 10)

# 83 CS0202 — GetEnumerator 만 있으면 순회가 될 줄 알았다.
ep('CS0202', 'Loot.cs',
   "foreach requires that 'Bag.GetEnumerator()' return a type with MoveNext and Current", """
using UnityEngine;

public class Bag
{
    public int[] items = { 1, 2 };
    public int GetEnumerator() => 0;
}

public class Loot : MonoBehaviour
{
    void Start()
    {
        Bag bag = new Bag();
        foreach (int n in bag)
        {
            Debug.Log(n);
        }
    }
}
""", """
using UnityEngine;

public class Bag
{
    public int[] items = { 1, 2 };
    public int GetEnumerator() => 0;
}

public class Loot : MonoBehaviour
{
    void Start()
    {
        Bag bag = new Bag();
        foreach (int n in bag.items)
        {
            Debug.Log(n);
        }
    }
}
""", 14)

# 84 CS0446 — 메서드를 부르지 않고 이름만 넘겼다.
ep('CS0446', 'Loot.cs',
   "Foreach cannot operate on a method group; did you mean to call it?", """
using UnityEngine;

public class Bag
{
    int[] items = { 1, 2 };

    public int[] Items() => items;
}

public class Loot : MonoBehaviour
{
    void Start()
    {
        Bag bag = new Bag();
        foreach (int n in bag.Items)
        {
            Debug.Log(n);
        }
    }
}
""", """
using UnityEngine;

public class Bag
{
    int[] items = { 1, 2 };

    public int[] Items() => items;
}

public class Loot : MonoBehaviour
{
    void Start()
    {
        Bag bag = new Bag();
        foreach (int n in bag.Items())
        {
            Debug.Log(n);
        }
    }
}
""", 15)

# 85 CS1515 — foreach 에서 in 을 빠뜨렸다.
ep('CS1515', 'Patrol.cs', "'in' expected", """
using UnityEngine;

public class Patrol : MonoBehaviour
{
    public Vector3[] path;

    void Start()
    {
        foreach (Vector3 spot path)
        {
            Debug.Log(spot);
        }
    }
}
""", """
using UnityEngine;

public class Patrol : MonoBehaviour
{
    public Vector3[] path;

    void Start()
    {
        foreach (Vector3 spot in path)
        {
            Debug.Log(spot);
        }
    }
}
""", 9)

# 86 CS0186 — 테스트하려고 대상을 null 로 바꿔둔 채 잊었다.
ep('CS0186', 'Loot.cs', "Use of null is not valid in this context", """
using UnityEngine;

public class Loot : MonoBehaviour
{
    public int[] drops = { 1, 2, 3 };

    void Start()
    {
        foreach (int n in null)
        {
            Debug.Log(n);
        }
    }
}
""", """
using UnityEngine;

public class Loot : MonoBehaviour
{
    public int[] drops = { 1, 2, 3 };

    void Start()
    {
        foreach (int n in drops)
        {
            Debug.Log(n);
        }
    }
}
""", 9)

# 87 CS1520 — 클래스 이름을 바꾸자 생성자가 이름 없는 메서드가 됐다.
ep('CS1520', 'Stats.cs', "Method must have a return type", """
using UnityEngine;

public class Stats : MonoBehaviour
{
    public int hp = 100;

    Player()
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

public class Stats : MonoBehaviour
{
    public int hp = 100;

    Stats()
    {
        hp = 100;
    }

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 7)

# 88 CS0270 — C 처럼 선언에 크기를 적었다.
ep('CS0270', 'Inventory.cs',
   "Array size cannot be specified in a variable declaration", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    int[3] slots;

    void Start()
    {
        slots[0] = 1;
        Debug.Log(slots[0]);
    }
}
""", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    int[] slots = new int[3];

    void Start()
    {
        slots[0] = 1;
        Debug.Log(slots[0]);
    }
}
""", 5)

# 89 CS1586 — 크기를 정하지 않고 배열을 만들었다.
ep('CS1586', 'Inventory.cs',
   "Array creation must have array size or array initializer", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    int[] slots;

    void Start()
    {
        slots = new int[];
        slots[0] = 1;
        Debug.Log(slots[0]);
    }
}
""", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    int[] slots;

    void Start()
    {
        slots = new int[3];
        slots[0] = 1;
        Debug.Log(slots[0]);
    }
}
""", 9)

# 90 CS0178 — 2차원 배열의 두 번째 크기를 비웠다.
ep('CS0178', 'Board.cs',
   "Invalid rank specifier: expected , or ]", """
using UnityEngine;

public class Board : MonoBehaviour
{
    int[,] grid;

    void Start()
    {
        grid = new int[3, ];
        grid[0, 0] = 1;
        Debug.Log(grid[0, 0]);
    }
}
""", """
using UnityEngine;

public class Board : MonoBehaviour
{
    int[,] grid;

    void Start()
    {
        grid = new int[3, 3];
        grid[0, 0] = 1;
        Debug.Log(grid[0, 0]);
    }
}
""", 9)

# 91 CS0650 — 자바처럼 이름 뒤에 대괄호를 붙였다.
ep('CS0650', 'Scores.cs',
   "Bad array declarator: put the rank specifier after the variable name", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    int best[5];

    void Start()
    {
        best[0] = 100;
        Debug.Log(best[0]);
    }
}
""", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    int[] best = new int[5];

    void Start()
    {
        best[0] = 100;
        Debug.Log(best[0]);
    }
}
""", 5)

# 92 CS0022 — 격자를 1차원으로 바꾸고 인덱싱을 안 고쳤다.
ep('CS0022', 'Board.cs',
   "Wrong number of indices inside [], expected 1", """
using UnityEngine;

public class Board : MonoBehaviour
{
    int[] cells = new int[9];

    void Start()
    {
        cells[1, 2] = 5;
        Debug.Log(cells[0]);
    }
}
""", """
using UnityEngine;

public class Board : MonoBehaviour
{
    int[] cells = new int[9];

    void Start()
    {
        cells[1] = 5;
        Debug.Log(cells[0]);
    }
}
""", 9)

# 93 CS0021 — 배열 대신 길이를 담은 변수를 인덱싱했다.
ep('CS0021', 'Scores.cs',
   "Cannot apply indexing with [] to an expression of type 'int'", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    int[] scores = { 90, 80, 70 };

    void Start()
    {
        int count = scores.Length;
        Debug.Log(count[0]);
    }
}
""", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    int[] scores = { 90, 80, 70 };

    void Start()
    {
        int count = scores.Length;
        Debug.Log(scores[0]);
    }
}
""", 10)

# 94 CS0443 — 줄을 복사하고 인덱스를 안 넣었다.
ep('CS0443', 'Scores.cs', "Syntax error; value expected", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    int[] hits = { 3, 7, 9 };

    void Start()
    {
        Debug.Log(hits[0]);
        Debug.Log(hits[1]);
        Debug.Log(hits[]);
    }
}
""", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    int[] hits = { 3, 7, 9 };

    void Start()
    {
        Debug.Log(hits[0]);
        Debug.Log(hits[1]);
        Debug.Log(hits[2]);
    }
}
""", 11)

# 95 CS0839 — 두 번째 인자를 비워둔 채 넘어갔다.
ep('CS0839', 'Weapon.cs', "Argument missing", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int shots, int power)
    {
        Debug.Log(shots * power);
    }

    void Update()
    {
        Fire(1, );
    }
}
""", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int shots, int power)
    {
        Debug.Log(shots * power);
    }

    void Update()
    {
        Fire(1, 10);
    }
}
""", 12)

# 96 CS1597 — C++ 습관으로 메서드 블록 뒤에 세미콜론을 찍었다.
ep('CS1597', 'Player.cs',
   "Semicolon after method or accessor block is not valid", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    void Heal()
    {
        hp = 100;
    };

    void Start()
    {
        Heal();
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    void Heal()
    {
        hp = 100;
    }

    void Start()
    {
        Heal();
    }
}
""", 10)

# 97 CS1527 — 네임스페이스 바로 밑 타입에 private 를 붙였다.
ep('CS1527', 'Types.cs',
   "Elements defined in a namespace cannot be explicitly declared as private", """
namespace Game
{
    private class Enemy
    {
        public int hp = 100;
    }

    public class Spawner
    {
        public int rate = 2;
    }
}
""", """
namespace Game
{
    class Enemy
    {
        public int hp = 100;
    }

    public class Spawner
    {
        public int rate = 2;
    }
}
""", 3)

# 98 CS1529 — 클래스를 쓰다가 using 을 그 자리에 추가했다.
ep('CS1529', 'Usings.cs',
   "A using clause must precede all other elements defined in the namespace", """
namespace Game
{
    public class Bag
    {
        public int size = 10;
    }

    using System;

    public class Chest
    {
        public int size = 20;
    }
}
""", """
namespace Game
{
    public class Bag
    {
        public int size = 10;
    }



    public class Chest
    {
        public int size = 20;
    }
}
""", 8)

# 99 CS1528 — 생성자처럼 괄호로 필드를 초기화했다.
ep('CS1528', 'Player.cs',
   "Expected ; or = after a field declaration", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;
    public int mana(50);
    public int attack = 20;

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
    public int mana = 50;
    public int attack = 20;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 6)

# 100 CS1585 — 한정자를 반환형 뒤에 붙였다.
ep('CS1585', 'Player.cs',
   "Member modifier must precede the member type and name", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    void public Heal()
    {
        hp = 100;
    }

    void Start()
    {
        Heal();
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    public void Heal()
    {
        hp = 100;
    }

    void Start()
    {
        Heal();
    }
}
""", 7)

# 101 CS0030 — 캐스트면 문자열도 숫자가 될 줄 알았다.
ep('CS0030', 'ScoreLoad.cs',
   "Cannot convert type 'string' to 'int'", """
using UnityEngine;

public class ScoreLoad : MonoBehaviour
{
    public string saved = "1200";

    void Start()
    {
        int best = (int)saved;
        Debug.Log(best);
    }
}
""", """
using UnityEngine;

public class ScoreLoad : MonoBehaviour
{
    public string saved = "1200";

    void Start()
    {
        int best = int.Parse(saved);
        Debug.Log(best);
    }
}
""", 9)

# 102 CS0031 — 색상값을 byte 에 담으면서 범위를 넘겼다.
ep('CS0031', 'Tint.cs',
   "Constant value '300' cannot be converted to a 'byte'", """
using UnityEngine;

public class Tint : MonoBehaviour
{
    public byte red = 255;
    public byte green = 300;
    public byte blue = 0;

    void Start()
    {
        Debug.Log(green);
    }
}
""", """
using UnityEngine;

public class Tint : MonoBehaviour
{
    public byte red = 255;
    public byte green = 200;
    public byte blue = 0;

    void Start()
    {
        Debug.Log(green);
    }
}
""", 6)

# 103 CS0037 — 값이 없다는 뜻으로 null 을 넣었다.
ep('CS0037', 'SaveSlot.cs',
   "Cannot convert null to 'int' because it is a non-nullable value type", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    public int lastScore = 0;

    public void Clear()
    {
        int score = null;
        lastScore = score;
    }
}
""", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    public int lastScore = 0;

    public void Clear()
    {
        int score = 0;
        lastScore = score;
    }
}
""", 9)

# 104 CS0039 — 필드를 너무 좁은 타입으로 선언해 두고 형제 타입으로 캐스트했다.
ep('CS0039', 'Shelter.cs',
   "Cannot convert type 'Dog' to 'Cat' via a reference conversion", """
using UnityEngine;

public class Animal : MonoBehaviour { }
public class Dog : Animal { }
public class Cat : Animal { }

public class Shelter : MonoBehaviour
{
    public Dog pet;

    void Start()
    {
        Cat cat = pet as Cat;
        Debug.Log(cat);
    }
}
""", """
using UnityEngine;

public class Animal : MonoBehaviour { }
public class Dog : Animal { }
public class Cat : Animal { }

public class Shelter : MonoBehaviour
{
    public Animal pet;

    void Start()
    {
        Cat cat = pet as Cat;
        Debug.Log(cat);
    }
}
""", 9)

# 105 CS0664 — 유니티에서 f 를 빠뜨렸다.
ep('CS0664', 'Movement.cs',
   "Literal of type double cannot be implicitly converted to 'float'; use an F suffix", """
using UnityEngine;

public class Movement : MonoBehaviour
{
    public float speed = 7.5;
    public float jump = 4f;

    void Update()
    {
        Debug.Log(speed);
    }
}
""", """
using UnityEngine;

public class Movement : MonoBehaviour
{
    public float speed = 7.5f;
    public float jump = 4f;

    void Update()
    {
        Debug.Log(speed);
    }
}
""", 5)

# 106 CS0221 — -1 을 없음 표시로 쓰려 했는데 부호 없는 타입이었다.
ep('CS0221', 'Counter.cs',
   "Constant value '-1' cannot be converted to a 'uint'", """
using UnityEngine;

public class Counter : MonoBehaviour
{
    public uint lives = 3;
    uint remaining = -1;

    void Start()
    {
        Debug.Log(remaining);
    }
}
""", """
using UnityEngine;

public class Counter : MonoBehaviour
{
    public uint lives = 3;
    uint remaining = 0;

    void Start()
    {
        Debug.Log(remaining);
    }
}
""", 6)

# 107 CS0220 — int 최대값에 1을 더했다.
ep('CS0220', 'Scores.cs',
   "The operation overflows at compile time in checked mode", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    public int maxScore = 2147483647;
    int guard = 2147483647 + 1;

    void Start()
    {
        Debug.Log(maxScore);
    }
}
""", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    public int maxScore = 2147483647;
    long guard = 2147483647L + 1;

    void Start()
    {
        Debug.Log(maxScore);
    }
}
""", 6)

# 108 CS0594 — 먼 거리를 적다가 지수를 과하게 키웠다.
ep('CS0594', 'CameraRig.cs',
   "Floating-point constant is outside the range of type 'float'", """
using UnityEngine;

public class CameraRig : MonoBehaviour
{
    public float farClip = 3.5e40f;
    public float nearClip = 0.1f;

    void Start()
    {
        Debug.Log(farClip);
    }
}
""", """
using UnityEngine;

public class CameraRig : MonoBehaviour
{
    public float farClip = 3.5e30f;
    public float nearClip = 0.1f;

    void Start()
    {
        Debug.Log(farClip);
    }
}
""", 5)

# 109 CS0595 — 지수 표기를 적다 말았다.
ep('CS0595', 'Spawner.cs', "Invalid real literal", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public float rate = 1.0e;
    public int total = 5;

    void Start()
    {
        Debug.Log(rate);
    }
}
""", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public float rate = 1.0e3f;
    public int total = 5;

    void Start()
    {
        Debug.Log(rate);
    }
}
""", 5)

# 110 CS0075 — 음수를 캐스트하면서 괄호를 안 씌웠다.
ep('CS0075', 'Cave.cs',
   "To cast a negative value, you must enclose the value in parentheses", """
using UnityEngine;

public struct Depth
{
    public int meters;

    public static explicit operator
        Depth(int depth) => new Depth();
}

public class Cave : MonoBehaviour
{
    void Start()
    {
        var below = (Depth)-1;
        Debug.Log(below.meters);
    }
}
""", """
using UnityEngine;

public struct Depth
{
    public int meters;

    public static explicit operator
        Depth(int depth) => new Depth();
}

public class Cave : MonoBehaviour
{
    void Start()
    {
        var below = (Depth)(-1);
        Debug.Log(below.meters);
    }
}
""", 15)

# 111 CS0077 — 값 타입을 as 로 꺼내려 했다.
ep('CS0077', 'SaveSlot.cs',
   "The as operator must be used with a reference type or nullable type", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    public object raw = 1;

    void Start()
    {
        int score = raw as int;
        Debug.Log(score);
    }
}
""", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    public object raw = 1;

    void Start()
    {
        int score = (int)raw;
        Debug.Log(score);
    }
}
""", 9)

# 112 CS0023 — 0이면 거짓이라는 C 습관이 나왔다.
ep('CS0023', 'Player.cs',
   "Operator '!' cannot be applied to operand of type 'int'", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    void Update()
    {
        bool dead = !hp;
        if (dead)
        {
            Destroy(gameObject);
        }
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    void Update()
    {
        bool dead = hp <= 0;
        if (dead)
        {
            Destroy(gameObject);
        }
    }
}
""", 9)

if __name__ == '__main__':
    write(E, 'tier2b.json')
