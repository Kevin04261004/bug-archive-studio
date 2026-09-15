# -*- coding: utf-8 -*-
"""3티어: var·익명 타입·const·기본값·ref/out·읽기 전용."""
from _common import make, write

E = {}
ep = make(E)

# 115 CS0172 — 부호 있는 값과 없는 값을 삼항으로 골랐다.
ep('CS0172', 'Score.cs',
   "Type of conditional expression cannot be determined", """
using UnityEngine;

public class Score : MonoBehaviour
{
    public bool won = true;
    public int gain = 10;
    public uint loss = 5;

    void Start()
    {
        var delta = won ? gain : loss;
        Debug.Log(delta);
    }
}
""", """
using UnityEngine;

public class Score : MonoBehaviour
{
    public bool won = true;
    public int gain = 10;
    public int loss = 5;

    void Start()
    {
        var delta = won ? gain : loss;
        Debug.Log(delta);
    }
}
""", 7)

# 116 CS0173 — 값이 없을 때만 문자열을 돌려주려 했다.
ep('CS0173', 'ScoreUI.cs',
   "Type of conditional expression cannot be determined between 'int' and 'string'", """
using UnityEngine;

public class ScoreUI : MonoBehaviour
{
    public bool ready = false;
    public int score = 120;

    void Start()
    {
        var text = ready ? score : "-";
        Debug.Log(text);
    }
}
""", """
using UnityEngine;

public class ScoreUI : MonoBehaviour
{
    public bool ready = false;
    public int score = 120;

    void Start()
    {
        var text = ready ? score : 0;
        Debug.Log(text);
    }
}
""", 10)

# 117 CS0815 — void 메서드가 결과를 돌려줄 거라 생각했다.
ep('CS0815', 'SaveSlot.cs',
   "Cannot assign void to an implicitly-typed variable", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    public int hp = 100;

    void ResetHp()
    {
        hp = 100;
    }

    void Start()
    {
        var result = ResetHp();
        Debug.Log("Reset done");
    }
}
""", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    public int hp = 100;

    void ResetHp()
    {
        hp = 100;
    }

    void Start()
    {
        ResetHp();
        Debug.Log("Reset done");
    }
}
""", 14)

# 118 CS0818 — var 로 선언만 해뒀다.
ep('CS0818', 'Combat.cs',
   "Implicitly-typed variables must be initialized", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    public int power = 10;

    public void Hit(bool critical)
    {
        var damage;
        if (critical)
        {
            damage = power * 2;
        }
        Debug.Log(damage);
    }
}
""", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    public int power = 10;

    public void Hit(bool critical)
    {
        var damage = power;
        if (critical)
        {
            damage = power * 2;
        }
        Debug.Log(damage);
    }
}
""", 9)

# 119 CS0819 — 한 줄에 var 로 두 개를 선언했다.
ep('CS0819', 'Board.cs',
   "Implicitly-typed variables cannot have multiple declarators", """
using UnityEngine;

public class Board : MonoBehaviour
{
    void Start()
    {
        var width = 3, height = 4;
        Debug.Log(width * height);
    }
}
""", """
using UnityEngine;

public class Board : MonoBehaviour
{
    void Start()
    {
        int width = 3, height = 4;
        Debug.Log(width * height);
    }
}
""", 7)

# 120 CS0820 — var 에 배열 초기화 구문을 바로 줬다.
ep('CS0820', 'Scores.cs',
   "Cannot initialize an implicitly-typed variable with an array initializer", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    void Start()
    {
        var hits = { 3, 7, 9 };
        Debug.Log(hits[0]);
    }
}
""", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    void Start()
    {
        var hits = new[] { 3, 7, 9 };
        Debug.Log(hits[0]);
    }
}
""", 7)

# 121 CS0821 — fixed 안에서 포인터 타입을 var 로 받으려 했다.
ep('CS0821', 'Pixels.cs',
   "A fixed statement cannot use an implicitly-typed local variable", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    int[] data = { 1, 2, 3 };

    unsafe void Scan()
    {
        fixed (var head = data)
        {
            Debug.Log(head[0]);
        }
    }
}
""", """
using UnityEngine;

public class Pixels : MonoBehaviour
{
    int[] data = { 1, 2, 3 };

    unsafe void Scan()
    {
        fixed (int* head = data)
        {
            Debug.Log(head[0]);
        }
    }
}
""", 9)

# 122 CS0822 — 상수를 var 로 선언했다.
ep('CS0822', 'Limits.cs',
   "Implicitly-typed variables cannot be constant", """
using UnityEngine;

public class Limits : MonoBehaviour
{
    void Start()
    {
        const var maxHp = 100;
        Debug.Log(maxHp);
    }
}
""", """
using UnityEngine;

public class Limits : MonoBehaviour
{
    void Start()
    {
        const int maxHp = 100;
        Debug.Log(maxHp);
    }
}
""", 7)

# 123 CS0825 — 필드를 var 로 선언했다.
ep('CS0825', 'Player.cs',
   "The contextual keyword var may only appear within a local variable declaration", """
using UnityEngine;

public class Player : MonoBehaviour
{
    var hp = 100;
    public int mana = 50;

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
    public int mana = 50;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 5)

# 124 CS0826 — 종류가 다른 값을 한 배열에 담았다.
ep('CS0826', 'Loot.cs',
   "No best type found for implicitly-typed array", """
using UnityEngine;

public class Loot : MonoBehaviour
{
    void Start()
    {
        var drops = new[] { 1, "gem" };
        Debug.Log(drops[0]);
    }
}
""", """
using UnityEngine;

public class Loot : MonoBehaviour
{
    void Start()
    {
        object[] drops = { 1, "gem" };
        Debug.Log(drops[0]);
    }
}
""", 7)

# 125 CS0828 — void 메서드 결과를 익명 타입에 담으려 했다.
ep('CS0828', 'Report.cs',
   "Cannot assign 'void' to anonymous type property", """
using UnityEngine;

public class Report : MonoBehaviour
{
    void Save()
    {
        Debug.Log("logged");
    }

    void Start()
    {
        var row = new { note = Save() };
        Debug.Log(row);
    }
}
""", """
using UnityEngine;

public class Report : MonoBehaviour
{
    void Save()
    {
        Debug.Log("logged");
    }

    void Start()
    {
        var row = new { note = "ok" };
        Debug.Log(row);
    }
}
""", 12)

# 126 CS0833 — 속성 이름을 바꾸지 않고 복사했다.
ep('CS0833', 'Report.cs',
   "An anonymous type cannot have multiple properties with the same name", """
using UnityEngine;

public class Report : MonoBehaviour
{
    void Start()
    {
        var row = new { id = 1, id = 2 };
        Debug.Log(row);
    }
}
""", """
using UnityEngine;

public class Report : MonoBehaviour
{
    void Start()
    {
        var row = new { id = 1, hp = 2 };
        Debug.Log(row);
    }
}
""", 7)

# 127 CS0836 — 익명 타입을 상수로 두려 했다.
ep('CS0836', 'Report.cs',
   "Cannot use anonymous type in a constant expression", """
using UnityEngine;

public class Report : MonoBehaviour
{
    void Start()
    {
        const object tag = new { id = 1 };
        Debug.Log(tag);
    }
}
""", """
using UnityEngine;

public class Report : MonoBehaviour
{
    void Start()
    {
        var tag = new { id = 1 };
        Debug.Log(tag);
    }
}
""", 7)

# 128 CS0841 — 아직 만들지 않은 지역 변수를 먼저 썼다.
ep('CS0841', 'Health.cs',
   "Cannot use local variable 'hp' before it is declared", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int max = 100;

    void Start()
    {
        Debug.Log("Start HP: " + hp);
        int hp = max;
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int max = 100;

    void Start()
    {
        Debug.Log("Start HP: " + max);
        int hp = max;
        Debug.Log(hp);
    }
}
""", 9)

# 129 CS0843 — 구조체 생성자에서 자동 속성을 채우지 않았다.
ep('CS0843', 'Bag.cs',
   "An auto-implemented property must be fully assigned before control is returned", """
using UnityEngine;

public struct Item
{
    public int Id { get; }

    public Item(int id)
    {
        Debug.Log(id);
    }
}

public class Bag : MonoBehaviour
{
    void Start()
    {
        var potion = new Item(1);
        Debug.Log(potion.Id);
    }
}
""", """
using UnityEngine;

public struct Item
{
    public int Id { get; }

    public Item(int id)
    {
        Id = id;
    }
}

public class Bag : MonoBehaviour
{
    void Start()
    {
        var potion = new Item(1);
        Debug.Log(potion.Id);
    }
}
""", 9)

# 130 CS0846 — 2차원 배열을 1차원처럼 초기화했다.
ep('CS0846', 'Board.cs', "A nested array initializer is expected", """
using UnityEngine;

public class Board : MonoBehaviour
{
    int[,] grid = { 1, 2 };

    void Start()
    {
        Debug.Log(grid[0, 0]);
    }
}
""", """
using UnityEngine;

public class Board : MonoBehaviour
{
    int[,] grid = { { 1, 2 } };

    void Start()
    {
        Debug.Log(grid[0, 0]);
    }
}
""", 5)

# 131 CS0847 — 크기는 3인데 값을 둘만 넣었다.
ep('CS0847', 'Scores.cs',
   "An array initializer of length 3 is expected", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    int[] hits = new int[3] { 1, 2 };

    void Start()
    {
        Debug.Log(hits[0]);
    }
}
""", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    int[] hits = new int[3] { 1, 2, 3 };

    void Start()
    {
        Debug.Log(hits[0]);
    }
}
""", 5)

# 132 CS0133 — 인스펙터 값으로 상수를 만들려 했다.
ep('CS0133', 'Limits.cs',
   "The expression being assigned to 'max' must be constant", """
using UnityEngine;

public class Limits : MonoBehaviour
{
    public int level = 2;

    void Start()
    {
        const int max = level * 10;
        Debug.Log(max);
    }
}
""", """
using UnityEngine;

public class Limits : MonoBehaviour
{
    public int level = 2;

    void Start()
    {
        int max = level * 10;
        Debug.Log(max);
    }
}
""", 9)

# 133 CS0134 — 배열을 const 로 두려 했다.
ep('CS0134', 'Limits.cs',
   "A const field of a reference type can only be initialized with null", """
using UnityEngine;

public class Limits : MonoBehaviour
{
    const int[] tiers = { 1, 2, 3 };

    void Start()
    {
        Debug.Log(tiers[0]);
    }
}
""", """
using UnityEngine;

public class Limits : MonoBehaviour
{
    static int[] tiers = { 1, 2, 3 };

    void Start()
    {
        Debug.Log(tiers[0]);
    }
}
""", 5)

# 134 CS0145 — const 를 선언만 하고 값을 안 줬다.
ep('CS0145', 'Limits.cs',
   "A const field requires a value to be provided", """
using UnityEngine;

public class Limits : MonoBehaviour
{
    const int maxHp;
    public int hp = 100;

    void Start()
    {
        Debug.Log(maxHp);
    }
}
""", """
using UnityEngine;

public class Limits : MonoBehaviour
{
    const int maxHp = 100;
    public int hp = 100;

    void Start()
    {
        Debug.Log(maxHp);
    }
}
""", 5)

# 135 CS0150 — case 에 인스펙터 필드를 썼다.
ep('CS0150', 'Difficulty.cs', "A constant value is expected", """
using UnityEngine;

public class Difficulty : MonoBehaviour
{
    public int limit = 3;

    public void Apply(int level)
    {
        switch (level)
        {
            case limit:
                Debug.Log("Capped");
                break;
        }
    }
}
""", """
using UnityEngine;

public class Difficulty : MonoBehaviour
{
    public int limit = 3;

    public void Apply(int level)
    {
        switch (level)
        {
            case 3:
                Debug.Log("Capped");
                break;
        }
    }
}
""", 11)

# 136 CS0110 — 두 상수가 서로를 가리킨다.
ep('CS0110', 'Limits.cs',
   "The evaluation of the constant value for 'MaxHp' involves a circular definition", """
using UnityEngine;

public class Limits : MonoBehaviour
{
    const int MaxHp = MaxMana;
    const int MaxMana = MaxHp;

    void Start()
    {
        Debug.Log(MaxHp);
    }
}
""", """
using UnityEngine;

public class Limits : MonoBehaviour
{
    const int MaxHp = MaxMana;
    const int MaxMana = 50;

    void Start()
    {
        Debug.Log(MaxHp);
    }
}
""", 6)

# 137 CS0283 — 구조체를 const 로 두려 했다.
ep('CS0283', 'SpawnPoint.cs',
   "The type 'Vector3' cannot be declared const", """
using UnityEngine;

public class SpawnPoint : MonoBehaviour
{
    const Vector3 origin = default;
    public int count = 3;

    void Start()
    {
        Debug.Log(origin);
    }
}
""", """
using UnityEngine;

public class SpawnPoint : MonoBehaviour
{
    static Vector3 origin = default;
    public int count = 3;

    void Start()
    {
        Debug.Log(origin);
    }
}
""", 5)

# 138 CS0463 — decimal 상수 계산이 범위를 넘었다.
ep('CS0463', 'Money.cs',
   "Evaluation of the decimal constant expression failed", """
using UnityEngine;

public class Money : MonoBehaviour
{
    const decimal total = 1e30m * 1e30m;
    public int gems = 500;

    void Start()
    {
        Debug.Log(total);
    }
}
""", """
using UnityEngine;

public class Money : MonoBehaviour
{
    const decimal total = 1e10m * 1e10m;
    public int gems = 500;

    void Start()
    {
        Debug.Log(total);
    }
}
""", 5)

# 139 CS1750 — 기본값으로 배열을 새로 만들려 했다.
ep('CS1750', 'Weapon.cs',
   "A value of type 'int[]' cannot be used as a default parameter", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int[] shots = new int[1])
    {
        Debug.Log(shots.Length);
    }

    void Start()
    {
        Fire();
    }
}
""", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int[] shots = null)
    {
        Debug.Log(shots.Length);
    }

    void Start()
    {
        Fire();
    }
}
""", 5)

# 140 CS1737 — 기본값 있는 매개변수를 앞에 뒀다.
ep('CS1737', 'Weapon.cs',
   "Optional parameters must appear after all required parameters", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int power = 1, int shots)
    {
        Debug.Log(power * shots);
    }

    void Start()
    {
        Fire(2, 3);
    }
}
""", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int power, int shots)
    {
        Debug.Log(power * shots);
    }

    void Start()
    {
        Fire(2, 3);
    }
}
""", 5)

# 141 CS1738 — 이름 붙인 인자를 앞에 두고 뒤는 그냥 넘겼다.
ep('CS1738', 'Weapon.cs',
   "Named argument specifications must appear after all fixed arguments", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int power, int shots)
    {
        Debug.Log(power * shots);
    }

    void Start()
    {
        Fire(power: 1, 2);
    }
}
""", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int power, int shots)
    {
        Debug.Log(power * shots);
    }

    void Start()
    {
        Fire(1, shots: 2);
    }
}
""", 12)

# 142 CS1739 — 매개변수 이름을 잘못 기억했다.
ep('CS1739', 'Weapon.cs',
   "The best overload for 'Fire' does not have a parameter named 'ammo'", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int power)
    {
        Debug.Log(power);
    }

    void Start()
    {
        Fire(ammo: 1);
    }
}
""", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int power)
    {
        Debug.Log(power);
    }

    void Start()
    {
        Fire(power: 1);
    }
}
""", 12)

# 143 CS1740 — 인자를 복사하고 이름을 안 바꿨다.
ep('CS1740', 'Weapon.cs',
   "Named argument 'power' cannot be specified multiple times", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int power, int shots)
    {
        Debug.Log(power * shots);
    }

    void Start()
    {
        Fire(power: 1, power: 2);
    }
}
""", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    void Fire(int power, int shots)
    {
        Debug.Log(power * shots);
    }

    void Start()
    {
        Fire(power: 1, shots: 2);
    }
}
""", 12)

# 144 CS1620 — ref 매개변수인데 그냥 넘겼다.
ep('CS1620', 'Health.cs',
   "Argument 1 must be passed with the 'ref' keyword", """
using UnityEngine;

public class Health : MonoBehaviour
{
    void Bump(ref int value)
    {
        value++;
    }

    void Start()
    {
        int hp = 1;
        Bump(hp);
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    void Bump(ref int value)
    {
        value++;
    }

    void Start()
    {
        int hp = 1;
        Bump(ref hp);
    }
}
""", 13)

# 145 CS1615 — ref 를 뗐는데 호출부에 남아 있다.
ep('CS1615', 'Health.cs',
   "Argument 1 may not be passed with the 'ref' keyword", """
using UnityEngine;

public class Health : MonoBehaviour
{
    void Bump(int value)
    {
        Debug.Log(value);
    }

    void Start()
    {
        int hp = 1;
        Bump(ref hp);
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    void Bump(int value)
    {
        Debug.Log(value);
    }

    void Start()
    {
        int hp = 1;
        Bump(hp);
    }
}
""", 13)

# 146 CS1510 — ref 자리에 상수를 넘겼다.
ep('CS1510', 'Health.cs',
   "A ref or out value must be an assignable variable", """
using UnityEngine;

public class Health : MonoBehaviour
{
    void Bump(ref int value)
    {
        value++;
    }

    void Start()
    {
        int hp = 1;
        Bump(ref 1);
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    void Bump(ref int value)
    {
        value++;
    }

    void Start()
    {
        int hp = 1;
        Bump(ref hp);
    }
}
""", 13)

# 147 CS0206 — 자동 속성을 ref 로 넘기려 했다.
ep('CS0206', 'Health.cs',
   "A property or indexer may not be passed as an out or ref parameter", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int Hp { get; set; }

    void Bump(ref int value)
    {
        value++;
    }

    void Start()
    {
        Bump(ref Hp);
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int Hp;

    void Bump(ref int value)
    {
        value++;
    }

    void Start()
    {
        Bump(ref Hp);
    }
}
""", 5)

# 148 CS0200 — get 만 있는 속성에 값을 넣었다.
ep('CS0200', 'Player.cs',
   "Property 'Player.Hp' cannot be assigned to; it is read only", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int Hp { get; }
    public int Mana { get; set; }

    void Start()
    {
        Hp = 50;
        Debug.Log(Hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int Hp { get; set; }
    public int Mana { get; set; }

    void Start()
    {
        Hp = 50;
        Debug.Log(Hp);
    }
}
""", 5)

# 149 CS1604 — foreach 변수를 그 자리에서 고치려 했다.
ep('CS1604', 'Loot.cs',
   "Cannot assign to 'drop' because it is a foreach iteration variable", """
using UnityEngine;

public class Loot : MonoBehaviour
{
    public int[] drops = { 1, 2, 3 };

    void Start()
    {
        int total = 0;
        foreach (int drop in drops)
        {
            drop = drop * 2;
        }
        Debug.Log(total);
    }
}
""", """
using UnityEngine;

public class Loot : MonoBehaviour
{
    public int[] drops = { 1, 2, 3 };

    void Start()
    {
        int total = 0;
        foreach (int drop in drops)
        {
            total += drop * 2;
        }
        Debug.Log(total);
    }
}
""", 12)

# 150 CS0191 — readonly 필드를 나중에 바꾸려 했다.
ep('CS0191', 'Player.cs',
   "A readonly field cannot be assigned to outside a constructor", """
using UnityEngine;

public class Player : MonoBehaviour
{
    readonly int maxHp = 100;

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
    int maxHp = 100;

    public void Rebalance()
    {
        maxHp = 50;
        Debug.Log(maxHp);
    }
}
""", 5)

# 151 CS0192 — readonly 필드를 ref 로 넘겼다.
ep('CS0192', 'Player.cs',
   "A readonly field cannot be passed as a ref or out argument", """
using UnityEngine;

public class Player : MonoBehaviour
{
    readonly int maxHp = 100;

    void Bump(ref int value)
    {
        value++;
    }

    void Start()
    {
        Bump(ref maxHp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int maxHp = 100;

    void Bump(ref int value)
    {
        value++;
    }

    void Start()
    {
        Bump(ref maxHp);
    }
}
""", 5)

if __name__ == '__main__':
    write(E, 'tier3a.json')
