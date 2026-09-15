# -*- coding: utf-8 -*-
"""1티어 리라이트. 실제로 일어나는 상황으로 다시 쓴 에피소드."""
import json, sys
from pathlib import Path

E = {}

def lines(block):
    # 앞의 빈 줄만 걷어내고, 끝은 마지막 개행 하나만 지운다: 의도한 빈 줄이 살아남는다
    return block.lstrip('\n').rstrip('\n').split('\n') if not block.endswith('\n\n') \
        else block.lstrip('\n')[:-1].rstrip('\n').split('\n') + ['']

def ep(code, filename, message, before, after, focus):
    E[code] = dict(filename=filename, message=message, focus_line=focus,
                   before=lines(before), after=lines(after))

# 1 CS0103 — 오타. 자동완성 없이 손으로 친 필드 이름이 한 글자 어긋난다.
ep('CS0103', 'ScoreUI.cs',
   "The name 'scroe' does not exist in the current context", """
using UnityEngine;

public class ScoreUI : MonoBehaviour
{
    public Text label;
    int score;

    public void AddPoints(int amount)
    {
        score += amount;
        label.text = "Score: " + scroe;
    }

    public void ResetScore()
    {
        score = 0;
        label.text = "Score: 0";
    }
}
""", """
using UnityEngine;

public class ScoreUI : MonoBehaviour
{
    public Text label;
    int score;

    public void AddPoints(int amount)
    {
        score += amount;
        label.text = "Score: " + score;
    }

    public void ResetScore()
    {
        score = 0;
        label.text = "Score: 0";
    }
}
""", 11)

# 2 CS0246 — 유니티가 넣어준 using System.Collections 로 List 가 될 줄 알았다.
ep('CS0246', 'Inventory.cs',
   "The type or namespace name 'List<>' could not be found (are you missing a using directive?)", """
using UnityEngine;
using System.Collections;

public class Inventory : MonoBehaviour
{
    List<string> items;

    void Start()
    {
        items = new List<string>();
        items.Add("Potion");
        items.Add("Sword");
    }

    public int SlotCount()
    {
        return items.Count;
    }
}
""", """
using UnityEngine;
using System.Collections.Generic;

public class Inventory : MonoBehaviour
{
    List<string> items;

    void Start()
    {
        items = new List<string>();
        items.Add("Potion");
        items.Add("Sword");
    }

    public int SlotCount()
    {
        return items.Count;
    }
}
""", 2)

# 3 CS1061 — 배열에 쓰던 Length 를 List 에 그대로 썼다.
ep('CS1061', 'ScoreBoard.cs',
   "'List<int>' does not contain a definition for 'Length' and no extension method was found", """
using UnityEngine;
using System.Collections.Generic;

public class ScoreBoard : MonoBehaviour
{
    List<int> scores = new List<int>();

    public void Submit(int score)
    {
        scores.Add(score);
        int shown = scores.Length;
        Debug.Log("Entries: " + shown);
    }

    public void Clear()
    {
        scores.Clear();
    }
}
""", """
using UnityEngine;
using System.Collections.Generic;

public class ScoreBoard : MonoBehaviour
{
    List<int> scores = new List<int>();

    public void Submit(int score)
    {
        scores.Add(score);
        int shown = scores.Count;
        Debug.Log("Entries: " + shown);
    }

    public void Clear()
    {
        scores.Clear();
    }
}
""", 11)

# 4 CS1002 — 디버그 로그를 급히 끼워 넣다가 세미콜론을 빠뜨렸다.
ep('CS1002', 'Player.cs', "; expected", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    public void TakeDamage(int amount)
    {
        hp -= amount;
        Debug.Log("HP left: " + hp)
        if (hp <= 0)
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

    public void TakeDamage(int amount)
    {
        hp -= amount;
        Debug.Log("HP left: " + hp);
        if (hp <= 0)
        {
            Destroy(gameObject);
        }
    }
}
""", 10)

# 5 CS1513 — for 블록을 감싸다가 닫는 중괄호를 지웠다.
ep('CS1513', 'Spawner.cs', "} expected", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public GameObject enemy;
    public int total = 5;

    void Start()
    {
        for (int i = 0; i < total; i++)
        {
            Instantiate(enemy);
            Debug.Log("Spawned " + i);

    }
}
""", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public GameObject enemy;
    public int total = 5;

    void Start()
    {
        for (int i = 0; i < total; i++)
        {
            Instantiate(enemy);
            Debug.Log("Spawned " + i);
        }
    }
}
""", 14)

# 6 CS1514 — 클래스 여는 중괄호가 통째로 날아갔다.
ep('CS1514', 'Stats.cs', "{ expected", """
using UnityEngine;

public class Stats : MonoBehaviour

    public int hp = 100;
    public int mana = 50;
    public float speed = 5f;

    public void ResetAll()
    {
        hp = 100;
        mana = 50;
    }
}
""", """
using UnityEngine;

public class Stats : MonoBehaviour
{
    public int hp = 100;
    public int mana = 50;
    public float speed = 5f;

    public void ResetAll()
    {
        hp = 100;
        mana = 50;
    }
}
""", 4)

# 7 CS1026 — 중첩 호출에서 안쪽 괄호만 닫았다.
ep('CS1026', 'Health.cs', ") expected", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 40;
    public int max = 100;

    public void AddHealth(int heal)
    {
        hp = Mathf.Min(hp + heal, max;
        Debug.Log("HP: " + hp);
    }

    public bool IsFull()
    {
        return hp == max;
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 40;
    public int max = 100;

    public void AddHealth(int heal)
    {
        hp = Mathf.Min(hp + heal, max);
        Debug.Log("HP: " + hp);
    }

    public bool IsFull()
    {
        return hp == max;
    }
}
""", 10)

# 8 CS1003 — 배열 초기화에 한 줄 추가하면서 앞 줄 쉼표를 안 찍었다.
ep('CS1003', 'WaveTable.cs', "Syntax error, ',' expected", """
using UnityEngine;

public class WaveTable : MonoBehaviour
{
    public int[] enemyCount =
    {
        5,
        10,
        20
        30,
        45,
    };

    public int CountFor(int wave)
    {
        return enemyCount[wave];
    }
}
""", """
using UnityEngine;

public class WaveTable : MonoBehaviour
{
    public int[] enemyCount =
    {
        5,
        10,
        20,
        30,
        45,
    };

    public int CountFor(int wave)
    {
        return enemyCount[wave];
    }
}
""", 9)

# 9 CS0029 — 인스펙터에 문자열로 둔 값을 int 에 그대로 넣었다.
ep('CS0029', 'ScoreLoad.cs',
   "Cannot implicitly convert type 'string' to 'int'", """
using UnityEngine;

public class ScoreLoad : MonoBehaviour
{
    public string savedBest = "1200";

    void Start()
    {
        int best = savedBest;
        Debug.Log("Best: " + best);
    }

    public void Save(int score)
    {
        savedBest = score.ToString();
    }
}
""", """
using UnityEngine;

public class ScoreLoad : MonoBehaviour
{
    public string savedBest = "1200";

    void Start()
    {
        int best = int.Parse(savedBest);
        Debug.Log("Best: " + best);
    }

    public void Save(int score)
    {
        savedBest = score.ToString();
    }
}
""", 9)

# 10 CS0266 — float 계산 결과를 int 에 그대로 받았다.
ep('CS0266', 'Movement.cs',
   "Cannot implicitly convert type 'float' to 'int'. An explicit conversion exists", """
using UnityEngine;

public class Movement : MonoBehaviour
{
    public float speed = 7.5f;
    public int tile = 2;

    void Update()
    {
        int steps = speed / tile;
        Debug.Log("Steps: " + steps);
    }

    public void Boost()
    {
        speed = speed * 2f;
    }
}
""", """
using UnityEngine;

public class Movement : MonoBehaviour
{
    public float speed = 7.5f;
    public int tile = 2;

    void Update()
    {
        int steps = (int)(speed / tile);
        Debug.Log("Steps: " + steps);
    }

    public void Boost()
    {
        speed = speed * 2f;
    }
}
""", 10)

# 11 CS0019 — 문자열 길이를 재려다 문자열 자체를 비교했다.
ep('CS0019', 'NameGate.cs',
   "Operator '>' cannot be applied to operands of type 'string' and 'int'", """
using UnityEngine;

public class NameGate : MonoBehaviour
{
    public string playerName = "Bug";

    public bool CanStart()
    {
        if (playerName > 3)
        {
            return true;
        }
        Debug.Log("Name too short");
        return false;
    }
}
""", """
using UnityEngine;

public class NameGate : MonoBehaviour
{
    public string playerName = "Bug";

    public bool CanStart()
    {
        if (playerName.Length > 3)
        {
            return true;
        }
        Debug.Log("Name too short");
        return false;
    }
}
""", 9)

# 12 CS0117 — C# 습관대로 Vector3.Zero 를 대문자로 썼다.
ep('CS0117', 'Resetter.cs',
   "'Vector3' does not contain a definition for 'Zero'", """
using UnityEngine;

public class Resetter : MonoBehaviour
{
    public Transform target;
    Vector3 startPoint;

    void Start()
    {
        startPoint = target.position;
    }

    public void ResetPosition()
    {
        target.position = Vector3.Zero;
        Debug.Log("Moved to origin");
    }
}
""", """
using UnityEngine;

public class Resetter : MonoBehaviour
{
    public Transform target;
    Vector3 startPoint;

    void Start()
    {
        startPoint = target.position;
    }

    public void ResetPosition()
    {
        target.position = Vector3.zero;
        Debug.Log("Moved to origin");
    }
}
""", 15)

# 13 CS0120 — 이벤트에 붙이려고 static 을 달았더니 필드를 못 읽는다.
ep('CS0120', 'GameFlow.cs',
   "An object reference is required for the non-static field 'GameFlow.score'", """
using UnityEngine;

public class GameFlow : MonoBehaviour
{
    int score;

    public void AddScore(int amount)
    {
        score += amount;
    }

    public static void ShowScore()
    {
        Debug.Log("Score: " + score);
    }
}
""", """
using UnityEngine;

public class GameFlow : MonoBehaviour
{
    int score;

    public void AddScore(int amount)
    {
        score += amount;
    }

    public void ShowScore()
    {
        Debug.Log("Score: " + score);
    }
}
""", 12)

# 14 CS0176 — 손에 인스턴스가 있으니 거기에 대고 static 메서드를 불렀다.
ep('CS0176', 'Wave.cs',
   "Member 'Enemy.ResetAll()' cannot be accessed with an instance reference", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public static void ResetAll()
    {
        Debug.Log("All enemies reset");
    }
}

public class Wave : MonoBehaviour
{
    public Enemy boss;

    public void StartWave()
    {
        boss.ResetAll();
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public static void ResetAll()
    {
        Debug.Log("All enemies reset");
    }
}

public class Wave : MonoBehaviour
{
    public Enemy boss;

    public void StartWave()
    {
        Enemy.ResetAll();
    }
}
""", 17)

# 15 CS0161 — if 두 개로 모든 경우를 덮었다고 생각했다.
ep('CS0161', 'Rewards.cs',
   "'Rewards.RewardFor(int)': not all code paths return a value", """
using UnityEngine;

public class Rewards : MonoBehaviour
{
    public int RewardFor(int rank)
    {
        if (rank == 1)
        {
            return 100;
        }
        if (rank == 2)
        {
            return 50;
        }

    }
}
""", """
using UnityEngine;

public class Rewards : MonoBehaviour
{
    public int RewardFor(int rank)
    {
        if (rank == 1)
        {
            return 100;
        }
        if (rank == 2)
        {
            return 50;
        }
        return 0;
    }
}
""", 15)

# 16 CS0165 — if 안에서만 값을 넣고 밖에서 썼다.
ep('CS0165', 'Combat.cs',
   "Use of unassigned local variable 'damage'", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    public int power = 10;

    public void Hit(bool critical)
    {
        int damage;
        if (critical)
        {
            damage = power * 2;
        }
        Debug.Log("Damage: " + damage);
    }
}
""", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    public int power = 10;

    public void Hit(bool critical)
    {
        int damage = power;
        if (critical)
        {
            damage = power * 2;
        }
        Debug.Log("Damage: " + damage);
    }
}
""", 9)

# 17 CS1501 — 인자를 받도록 고쳐놓고 호출부를 안 고쳤다.
ep('CS1501', 'Weapon.cs',
   "No overload for method 'Fire' takes 0 arguments", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    public int power = 10;
    public int ammo = 30;

    void Fire(int shots)
    {
        ammo -= shots;
        Debug.Log(shots * power);
    }

    void Update()
    {
        Fire();
    }
}
""", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    public int power = 10;
    public int ammo = 30;

    void Fire(int shots)
    {
        ammo -= shots;
        Debug.Log(shots * power);
    }

    void Update()
    {
        Fire(1);
    }
}
""", 16)

# 18 CS1503 — 인스펙터에 문자열로 둔 대기 시간을 float 매개변수에 넘겼다.
ep('CS1503', 'Timers.cs',
   "Argument 1: cannot convert from 'string' to 'float'", """
using UnityEngine;

public class Timers : MonoBehaviour
{
    public string waitText = "3";

    void Wait(float seconds)
    {
        Debug.Log("Waiting " + seconds);
    }

    void Start()
    {
        Wait(waitText);
    }
}
""", """
using UnityEngine;

public class Timers : MonoBehaviour
{
    public string waitText = "3";

    void Wait(float seconds)
    {
        Debug.Log("Waiting " + seconds);
    }

    void Start()
    {
        Wait(float.Parse(waitText));
    }
}
""", 14)

# 19 CS1729 — 생성자에 매개변수를 넣고 나서 필드 초기화를 그대로 뒀다.
ep('CS1729', 'Spawner.cs',
   "'Enemy' does not contain a constructor that takes 0 arguments", """
public class Enemy
{
    public int hp;

    public Enemy(int startHp)
    {
        hp = startHp;
    }
}

public class EnemyPool
{
    Enemy boss = new Enemy();

    public int BossHp()
    {
        return boss.hp;
    }
}
""", """
public class Enemy
{
    public int hp;

    public Enemy(int startHp)
    {
        hp = startHp;
    }
}

public class EnemyPool
{
    Enemy boss = new Enemy(500);

    public int BossHp()
    {
        return boss.hp;
    }
}
""", 13)

# 20 CS7036 — 필수 인자를 안 넘겼다.
ep('CS7036', 'Enemy.cs',
   "There is no argument given that corresponds to the required parameter 'damage'", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    void TakeHit(int damage)
    {
        hp -= damage;
        if (hp <= 0)
        {
            Destroy(gameObject);
        }
    }

    void OnTriggerEnter()
    {
        TakeHit();
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    void TakeHit(int damage)
    {
        hp -= damage;
        if (hp <= 0)
        {
            Destroy(gameObject);
        }
    }

    void OnTriggerEnter()
    {
        TakeHit(10);
    }
}
""", 18)

# 21 CS0128 — 윗줄을 복사해 붙이면서 타입까지 같이 따라왔다.
ep('CS0128', 'Stats.cs',
   "A local variable named 'hp' is already defined in this scope", """
using UnityEngine;

public class Stats : MonoBehaviour
{
    public int armor = 5;

    void Start()
    {
        int hp = 100;
        Debug.Log("Start HP: " + hp);

        hp = hp - armor;
        int hp = hp + 10;
        Debug.Log("Final HP: " + hp);
    }
}
""", """
using UnityEngine;

public class Stats : MonoBehaviour
{
    public int armor = 5;

    void Start()
    {
        int hp = 100;
        Debug.Log("Start HP: " + hp);

        hp = hp - armor;
        hp = hp + 10;
        Debug.Log("Final HP: " + hp);
    }
}
""", 13)

# 22 CS0136 — 위에서 쓴 이름을 for 문에서 다시 선언했다.
ep('CS0136', 'GridBuilder.cs',
   "A local or parameter named 'i' cannot be declared in this scope", """
using UnityEngine;

public class GridBuilder : MonoBehaviour
{
    public int size = 3;

    void Build()
    {
        int i = size * size;
        Debug.Log("Total tiles: " + i);

        for (int i = 0; i < size; i++)
        {
            Debug.Log("Row placed");
        }
    }
}
""", """
using UnityEngine;

public class GridBuilder : MonoBehaviour
{
    public int size = 3;

    void Build()
    {
        int i = size * size;
        Debug.Log("Total tiles: " + i);

        for (int x = 0; x < size; x++)
        {
            Debug.Log("Row placed");
        }
    }
}
""", 12)

# 23 CS0101 — 파일을 복제하고 클래스 이름을 안 바꿨다.
ep('CS0101', 'Enemies.cs',
   "The namespace 'Game' already contains a definition for 'Enemy'", """
namespace Game
{
    public class Enemy
    {
        public int hp = 100;
        public int damage = 10;
    }

    public class Enemy
    {
        public int hp = 500;
        public int damage = 40;
    }
}
""", """
namespace Game
{
    public class Enemy
    {
        public int hp = 100;
        public int damage = 10;
    }

    public class Boss
    {
        public int hp = 500;
        public int damage = 40;
    }
}
""", 9)

# 24 CS0111 — 매개변수 이름만 바꾼 오버로드는 오버로드가 아니다.
ep('CS0111', 'Weapon.cs',
   "Type 'Weapon' already defines a member called 'Fire' with the same parameter types", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    public int ammo = 30;

    public void Fire(int shots)
    {
        ammo -= shots;
    }

    public void Fire(int count)
    {
        ammo -= count * 3;
        Debug.Log("Burst fired");
    }
}
""", """
using UnityEngine;

public class Weapon : MonoBehaviour
{
    public int ammo = 30;

    public void Fire(int shots)
    {
        ammo -= shots;
    }

    public void FireBurst(int count)
    {
        ammo -= count * 3;
        Debug.Log("Burst fired");
    }
}
""", 12)

# 25 CS0102 — 리팩터링 중에 같은 이름 필드를 하나 더 만들었다.
ep('CS0102', 'Player.cs',
   "The type 'Player' already contains a definition for 'hp'", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;
    public int mana = 50;
    public float speed = 5f;
    public float hp = 100f;

    void Start()
    {
        Debug.Log("HP " + hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;
    public int mana = 50;
    public float speed = 5f;
    public float shield = 100f;

    void Start()
    {
        Debug.Log("HP " + hp);
    }
}
""", 8)

# 26 CS0106 — 메서드 안의 지역 함수에 습관적으로 public 을 붙였다.
ep('CS0106', 'Helpers.cs',
   "The modifier 'public' is not valid for this item", """
using UnityEngine;

public class Helpers : MonoBehaviour
{
    void Start()
    {
        int total = Double(21);
        Debug.Log("Total: " + total);

        public int Double(int value)
        {
            return value * 2;
        }
    }
}
""", """
using UnityEngine;

public class Helpers : MonoBehaviour
{
    void Start()
    {
        int total = Double(21);
        Debug.Log("Total: " + total);

        int Double(int value)
        {
            return value * 2;
        }
    }
}
""", 10)

# 27 CS0116 — 상수를 클래스 밖 네임스페이스에 바로 뒀다.
ep('CS0116', 'Game.cs',
   "A namespace cannot directly contain members such as fields or methods", """
namespace Game
{
    public class Enemy
    {
        public int hp = 100;
    }

    const int Max = 20;

    public class Spawner
    {
        public int rate = 2;
    }
}
""", """
namespace Game
{
    public class Enemy
    {
        public int hp = 100;
    }

    class Limits { const int Max = 20; }

    public class Spawner
    {
        public int rate = 2;
    }
}
""", 8)

# 28 CS0122 — 인스펙터에 안 띄우려고 public 을 뺐더니 다른 스크립트가 못 읽는다.
ep('CS0122', 'HpBar.cs',
   "'Enemy.hp' is inaccessible due to its protection level", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    int hp = 100;

    public void Hit(int damage)
    {
        hp -= damage;
    }
}

public class HpBar : MonoBehaviour
{
    public Enemy target;
    void Update()
    {
        Debug.Log(target.hp);
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int hp = 100;

    public void Hit(int damage)
    {
        hp -= damage;
    }
}

public class HpBar : MonoBehaviour
{
    public Enemy target;
    void Update()
    {
        Debug.Log(target.hp);
    }
}
""", 5)

# 29 CS0201 — 더한 값을 어디에도 넣지 않았다.
ep('CS0201', 'Player.cs',
   "Only assignment, call, increment or new object expressions can be a statement", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    public void Heal(int amount)
    {
        Debug.Log("Healing " + amount);
        hp + amount;
        Debug.Log("HP now " + hp);
    }

    public void Kill()
    {
        hp = 0;
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    public void Heal(int amount)
    {
        Debug.Log("Healing " + amount);
        hp += amount;
        Debug.Log("HP now " + hp);
    }

    public void Kill()
    {
        hp = 0;
    }
}
""", 10)

# 30 CS1519 — 필드에서 타입을 빠뜨렸다.
ep('CS1519', 'Player.cs',
   "Invalid token '=' in class, record, struct, or interface member declaration", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;
    public float speed = 5f;
    public name = "Hero";
    public bool alive = true;

    void Start()
    {
        Debug.Log(name);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;
    public float speed = 5f;
    public string name = "Hero";
    public bool alive = true;

    void Start()
    {
        Debug.Log(name);
    }
}
""", 7)

# 31 CS1525 — 세 번째 성분을 비워둔 채 괄호를 닫았다.
ep('CS1525', 'Mover.cs',
   "Invalid expression term ')'", """
using UnityEngine;

public class Mover : MonoBehaviour
{
    public float speed = 3f;

    void Update()
    {
        var dir = new Vector3(1, 0, );
        dir *= speed * Time.deltaTime;
        transform.Translate(dir);
    }

    public void Stop()
    {
        speed = 0f;
    }
}
""", """
using UnityEngine;

public class Mover : MonoBehaviour
{
    public float speed = 3f;

    void Update()
    {
        var dir = new Vector3(1, 0, 0);
        dir *= speed * Time.deltaTime;
        transform.Translate(dir);
    }

    public void Stop()
    {
        speed = 0f;
    }
}
""", 9)

# 32 CS0234 — UI 타입이 UnityEngine 바로 밑에 있는 줄 알았다.
ep('CS0234', 'HudText.cs',
   "The type or namespace name 'Text' does not exist in the namespace 'UnityEngine'", """
using UnityEngine;

public class HudText : MonoBehaviour
{
    public UnityEngine.Text label;
    public int lives = 3;

    void Start()
    {
        label.text = "Lives: " + lives;
    }

    public void LoseLife()
    {
        lives--;
    }
}
""", """
using UnityEngine;

public class HudText : MonoBehaviour
{
    public UnityEngine.UI.Text label;
    public int lives = 3;

    void Start()
    {
        label.text = "Lives: " + lives;
    }

    public void LoseLife()
    {
        lives--;
    }
}
""", 5)

# 33 CS1022 — 메서드를 지우면서 닫는 중괄호가 하나 남았다.
ep('CS1022', 'Player.cs',
   "Type or namespace definition, or end-of-file expected", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    public void Heal(int amount)
    {
        hp += amount;
        Debug.Log("HP: " + hp);
    }
}
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;

    public void Heal(int amount)
    {
        hp += amount;
        Debug.Log("HP: " + hp);
    }
}

""" + "\n", 13)

# 34 CS0017 — 예제 코드를 프로젝트에 그대로 붙여 넣었다.
ep('CS0017', 'Program.cs',
   "Program has more than one entry point defined", """
using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Game start");
    }
}

class TestRunner
{
    static void Main()
    {
        Console.WriteLine("Tests done");
    }
}
""", """
using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Game start");
    }
}

class TestRunner
{
    static void RunAll()
    {
        Console.WriteLine("Tests done");
    }
}
""", 13)

if __name__ == '__main__':
    out = Path(sys.argv[1] if len(sys.argv) > 1 else 'tools/batches/tier1.json')
    out.write_text(json.dumps(E, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'{len(E)}편 -> {out}')
