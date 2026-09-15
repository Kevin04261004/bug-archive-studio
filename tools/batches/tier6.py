# -*- coding: utf-8 -*-
"""이터레이터 나머지·using·nullable·switch 식·최신 문법·경고."""
from _common import make, write

E = {}
ep = make(E)

# 361 CS1626 — catch 가 붙은 try 안에서 yield 했다.
ep('CS1626', 'Waves.cs',
   "Cannot yield a value in the body of a try block with a catch clause", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts()
    {
        try
        {
            yield return 1;
        }
        catch
        {
            Debug.Log("failed");
        }
    }
}
""", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts()
    {
        try
        {
            Debug.Log(1);
        }
        catch
        {
            Debug.Log("failed");
        }
    }
}
""", 10)

# 362 CS1627 — yield return 뒤에 값을 안 적었다.
ep('CS1627', 'Waves.cs', "Expression expected after yield return", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts()
    {
        yield return 1;
        yield return 2;
        yield return;
    }
}
""", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts()
    {
        yield return 1;
        yield return 2;
        yield break;
    }
}
""", 10)

# 363 CS1631 — catch 안에서 yield 했다.
ep('CS1631', 'Waves.cs',
   "Cannot yield a value in the body of a catch clause", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts()
    {
        yield return 1;

        try
        {
        }
        catch
        {
            yield return 2;
        }
    }
}
""", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts()
    {
        yield return 1;

        try
        {
        }
        catch
        {
            Debug.Log("failed");
        }
    }
}
""", 15)

# 364 CS1636 — 이터레이터에 __arglist 를 뒀다.
ep('CS1636', 'Waves.cs',
   "__arglist is not allowed in the parameter list of iterators", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts(__arglist)
    {
        yield return 1;
        yield return 2;
    }
}
""", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts()
    {
        yield return 1;
        yield return 2;
    }
}
""", 6)

# 365 CS1637 — 이터레이터에 포인터 매개변수를 뒀다.
ep('CS1637', 'Waves.cs',
   "Iterators cannot have unsafe parameters or yield types", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts(int* raw)
    {
        yield return 1;
        yield return 2;
    }
}
""", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts(int raw)
    {
        yield return 1;
        yield return 2;
    }
}
""", 6)

# 366 CS1643 — 람다에서 값을 안 돌려주는 경로가 있다.
ep('CS1643', 'Score.cs',
   "Not all code paths return a value in lambda expression of type 'Func<int>'", """
using System;
using UnityEngine;

public class Score : MonoBehaviour
{
    void Start()
    {
        Func<int> best = () =>
        {
            int total = 1200;

        };
        Debug.Log(best());
    }
}
""", """
using System;
using UnityEngine;

public class Score : MonoBehaviour
{
    void Start()
    {
        Func<int> best = () =>
        {
            int total = 1200;
            return total;
        };
        Debug.Log(best());
    }
}
""", 11)

# 367 CS1674 — IDisposable 이 아닌 타입에 using 을 썼다.
ep('CS1674', 'Game.cs',
   "'Player': type used in a using statement must be convertible to IDisposable", """
using UnityEngine;

public class Player
{
    public int hp;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        using (var hero = new Player())
        {
            Debug.Log(hero.hp);
        }
    }
}
""", """
using UnityEngine;

public class Player
{
    public int hp;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        var hero = new Player();
        {
            Debug.Log(hero.hp);
        }
    }
}
""", 12)

# 368 CS0210 — using 선언에 값을 안 줬다.
ep('CS0210', 'SaveFile.cs',
   "You must provide an initializer in a fixed or using statement declaration", """
using System.IO;
using UnityEngine;

public class SaveFile : MonoBehaviour
{
    void Load()
    {
        using (Stream data)
        {
            Debug.Log(data);
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
        using (Stream data = null)
        {
            Debug.Log(data);
        }
    }
}
""", 8)

# 369 CS8600 — null 일 수 있는 값을 그냥 받았다.
ep('CS8600', 'SaveSlot.cs',
   "Converting null literal or possible null value to non-nullable type", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        string? saved = null;
        string name = saved;
        Debug.Log(name);
    }
}
""", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        string? saved = null;
        string name = saved ?? "";
        Debug.Log(name);
    }
}
""", 9)

# 370 CS8601 — null 일 수 있는 값을 필드에 넣었다.
ep('CS8601', 'Game.cs', "Possible null reference assignment", """
#nullable enable
using UnityEngine;

public class Player
{
    public string name = "";
}

public class Game : MonoBehaviour
{
    void Rename(Player who, string? text)
    {
        who.name = text;
    }
}
""", """
#nullable enable
using UnityEngine;

public class Player
{
    public string name = "";
}

public class Game : MonoBehaviour
{
    void Rename(Player who, string? text)
    {
        who.name = text ?? "";
    }
}
""", 13)

# 371 CS8602 — null 일 수 있는 값의 멤버를 읽었다.
ep('CS8602', 'SaveSlot.cs', "Dereference of a possibly null reference", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        string? saved = null;
        Debug.Log(saved.Length);
    }
}
""", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        string? saved = null;
        Debug.Log(saved?.Length);
    }
}
""", 9)

# 372 CS8603 — null 을 돌려줬다.
ep('CS8603', 'SaveSlot.cs', "Possible null reference return", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    string Load()
    {
        return null;
    }

    void Start()
    {
        Debug.Log(Load());
    }
}
""", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    string Load()
    {
        return "";
    }

    void Start()
    {
        Debug.Log(Load());
    }
}
""", 8)

# 373 CS8604 — null 일 수 있는 값을 인자로 넘겼다.
ep('CS8604', 'SaveSlot.cs',
   "Possible null reference argument for parameter 'text'", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Show(string text)
    {
        Debug.Log(text);
    }

    void Start()
    {
        string? saved = null;
        Show(saved);
    }
}
""", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Show(string text)
    {
        Debug.Log(text);
    }

    void Start()
    {
        string? saved = null;
        Show(saved ?? "");
    }
}
""", 14)

# 374 CS8618 — non-nullable 필드를 안 채웠다.
ep('CS8618', 'Player.cs',
   "Non-nullable field 'playerName' must contain a non-null value", """
#nullable enable
using UnityEngine;

public class Player : MonoBehaviour
{
    public string playerName;
    public int hp = 100;

    void Start()
    {
        Debug.Log(playerName);
    }
}
""", """
#nullable enable
using UnityEngine;

public class Player : MonoBehaviour
{
    public string playerName = "";
    public int hp = 100;

    void Start()
    {
        Debug.Log(playerName);
    }
}
""", 6)

# 375 CS8619 — 제네릭 인자의 null 허용 여부가 다르다.
ep('CS8619', 'Inventory.cs',
   "Nullability of 'List<string?>' does not match target type 'List<string>'", """
#nullable enable
using System.Collections.Generic;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    void Start()
    {
        var raw = new List<string?>();
        List<string> items = raw;
        Debug.Log(items.Count);
    }
}
""", """
#nullable enable
using System.Collections.Generic;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    void Start()
    {
        var raw = new List<string?>();
        List<string?> items = raw;
        Debug.Log(items.Count);
    }
}
""", 10)

# 376 CS8620 — 인자의 null 허용 여부가 매개변수와 다르다.
ep('CS8620', 'Inventory.cs',
   "Argument of type 'List<string?>' cannot be used for parameter 'items'", """
#nullable enable
using System.Collections.Generic;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    void Show(List<string> items)
    {
        Debug.Log(items.Count);
    }

    void Start()
    {
        var raw = new List<string?>();
        Show(raw);
    }
}
""", """
#nullable enable
using System.Collections.Generic;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    void Show(List<string?> items)
    {
        Debug.Log(items.Count);
    }

    void Start()
    {
        var raw = new List<string?>();
        Show(raw);
    }
}
""", 7)

# 377 CS8625 — non-nullable 변수에 null 을 넣었다.
ep('CS8625', 'SaveSlot.cs',
   "Cannot convert null literal to non-nullable reference type", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        string saved = null;
        Debug.Log(saved);
    }
}
""", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        string? saved = null;
        Debug.Log(saved);
    }
}
""", 8)

# 378 CS8629 — nullable 값 타입을 그냥 캐스트했다.
ep('CS8629', 'SaveSlot.cs', "Nullable value type may be null", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        int? saved = null;
        int score = (int)saved;
        Debug.Log(score);
    }
}
""", """
#nullable enable
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        int? saved = null;
        int score = saved ?? 0;
        Debug.Log(score);
    }
}
""", 9)

# 379 CS8632 — nullable 문맥 밖에서 ? 를 썼다.
ep('CS8632', 'Player.cs',
   "The ? annotation should only be used in code within a #nullable context", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public string? playerName;
    public int hp = 100;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public string playerName;
    public int hp = 100;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 5)

# 380 CS8714 — notnull 제약에 nullable 을 넣었다.
ep('CS8714', 'Bag.cs',
   "The type 'string?' does not match the 'notnull' constraint on type parameter 'T'", """
#nullable enable
using UnityEngine;

public class Box<T> where T : notnull
{
    public T item;
}

public class Bag : MonoBehaviour
{
    Box<string?> box = new();
}
""", """
#nullable enable
using UnityEngine;

public class Box<T> where T : notnull
{
    public T item;
}

public class Bag : MonoBehaviour
{
    Box<string> box = new();
}
""", 11)

# 381 CS8509 — switch 식이 모든 경우를 덮지 않는다.
ep('CS8509', 'Rewards.cs',
   "The switch expression does not handle all possible values of its input type", """
using UnityEngine;

public class Rewards : MonoBehaviour
{
    int Bonus(int rank) => rank switch
    {
        1 => 100,
        2 => 50,

    };

    void Start()
    {
        Debug.Log(Bonus(1));
    }
}
""", """
using UnityEngine;

public class Rewards : MonoBehaviour
{
    int Bonus(int rank) => rank switch
    {
        1 => 100,
        2 => 50,
        _ => 0,
    };

    void Start()
    {
        Debug.Log(Bonus(1));
    }
}
""", 9)

# 382 CS8524 — enum 값을 다 덮지 않았다.
ep('CS8524', 'Rewards.cs',
   "The switch expression does not handle some values of its input type 'Team'", """
using UnityEngine;

public enum Team { Red, Blue }

public class Rewards : MonoBehaviour
{
    int Bonus(Team team) => team switch
    {
        Team.Red => 1,
        Team.Blue => 2,

    };

    void Start()
    {
        Debug.Log(Bonus(Team.Red));
    }
}
""", """
using UnityEngine;

public enum Team { Red, Blue }

public class Rewards : MonoBehaviour
{
    int Bonus(Team team) => team switch
    {
        Team.Red => 1,
        Team.Blue => 2,
        _ => 0,
    };

    void Start()
    {
        Debug.Log(Bonus(Team.Red));
    }
}
""", 11)

# 383 CS8510 — 같은 패턴을 두 번 적었다.
ep('CS8510', 'Rewards.cs',
   "The pattern is unreachable; it has already been handled by a previous arm", """
using UnityEngine;

public class Rewards : MonoBehaviour
{
    int Bonus(int rank) => rank switch
    {
        1 => 100,
        1 => 50,
        _ => 0,
    };

    void Start()
    {
        Debug.Log(Bonus(1));
    }
}
""", """
using UnityEngine;

public class Rewards : MonoBehaviour
{
    int Bonus(int rank) => rank switch
    {
        1 => 100,
        2 => 50,
        _ => 0,
    };

    void Start()
    {
        Debug.Log(Bonus(1));
    }
}
""", 8)

# 384 CS8652 — 프로젝트가 지원하지 않는 최신 문법을 썼다.
ep('CS8652', 'Scores.cs',
   "The feature 'collection expressions' is currently in Preview and unsupported", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    void Start()
    {
        int[] best = [90, 80, 70];
        Debug.Log(best[0]);
    }
}
""", """
using UnityEngine;

public class Scores : MonoBehaviour
{
    void Start()
    {
        int[] best = { 90, 80, 70 };
        Debug.Log(best[0]);
    }
}
""", 7)

# 385 CS8400 — 언어 버전이 낮은데 ^ 인덱스를 썼다.
ep('CS8400', 'Names.cs',
   "Feature 'index operator' is not available in C# 7.3; use version 8.0 or greater", """
using UnityEngine;

public class Names : MonoBehaviour
{
    public string playerName = "Bug";

    void Start()
    {
        char last = playerName[^1];
        Debug.Log(last);
    }
}
""", """
using UnityEngine;

public class Names : MonoBehaviour
{
    public string playerName = "Bug";

    void Start()
    {
        char last = playerName[2];
        Debug.Log(last);
    }
}
""", 9)

# 386 CS8803 — 타입 선언 뒤에 최상위 문을 더 썼다.
ep('CS8803', 'Program.cs',
   "Top-level statements must precede namespace and type declarations", """
using System;

Console.WriteLine("start");

class Player
{
    public int hp = 100;
}

Console.WriteLine("end");

class Enemy
{
    public int hp = 50;
}
""", """
using System;

Console.WriteLine("start");

class Player
{
    public int hp = 100;
}



class Enemy
{
    public int hp = 50;
}
""", 10)

# 388 CS8862 — 기본 생성자가 주 생성자를 안 불렀다.
ep('CS8862', 'Player.cs',
   "A constructor in a type with a parameter list must have a this constructor initializer", """
using UnityEngine;

public class Player(int hp)
{
    public int Hp = hp;

    public Player()
    {
        Debug.Log("default");
    }
}
""", """
using UnityEngine;

public class Player(int hp)
{
    public int Hp = hp;

    public Player() : this(100)
    {
        Debug.Log("default");
    }
}
""", 7)

# 389 CS8865 — 레코드를 클래스로 상속했다.
ep('CS8865', 'Boss.cs', "Only records may inherit from records", """
using UnityEngine;

public record Unit
{
    public int hp;
}

public class Boss : Unit
{
    public int shield;
}
""", """
using UnityEngine;

public record Unit
{
    public int hp;
}

public record Boss : Unit
{
    public int shield;
}
""", 8)

# 390 CS8866 — 위치 매개변수와 같은 이름의 필드를 뒀다.
ep('CS8866', 'Unit.cs',
   "Record member 'Unit.hp' must be a readable instance property to match parameter 'hp'", """
using UnityEngine;

public record Unit(int hp)
{
    public int hp;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(new Unit(1).hp);
    }
}
""", """
using UnityEngine;

public record Unit(int hp)
{
    public int hp { get; init; }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(new Unit(1).hp);
    }
}
""", 5)

# 391 CS9035 — required 멤버를 안 채웠다.
ep('CS9035', 'Game.cs',
   "Required member 'Player.playerName' must be set in the object initializer", """
using UnityEngine;

public class Player
{
    public required string playerName;
    public int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        var hero = new Player();
        Debug.Log(hero.hp);
    }
}
""", """
using UnityEngine;

public class Player
{
    public string playerName = "";
    public int hp = 100;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        var hero = new Player();
        Debug.Log(hero.hp);
    }
}
""", 5)

# 392 CS8641 — if 와 else 사이에 문장을 끼워 넣었다.
ep('CS8641', 'Health.cs', "'else' cannot start a statement", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        if (hp > 50)
            Debug.Log("ok");
        Debug.Log("checked");
        else
            Debug.Log("low");
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        if (hp > 50)
            Debug.Log("ok");

        else
            Debug.Log("low");
    }
}
""", 11)

# 393 CS0472 — 값 타입을 null 과 비교했다.
ep('CS0472', 'Health.cs',
   "The result is always true since a value of type 'int' is never equal to null", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        if (hp != null)
        {
            Debug.Log("alive");
        }
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
        {
            Debug.Log("alive");
        }
    }
}
""", 9)

# 394 CS0183 — 항상 참인 is 검사를 했다.
ep('CS0183', 'SaveSlot.cs',
   "The given expression is always of the provided type 'object'", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    public string saved = "1200";

    void Start()
    {
        if (saved is object)
        {
            Debug.Log(saved);
        }
    }
}
""", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    public string saved = "1200";

    void Start()
    {
        if (saved != null)
        {
            Debug.Log(saved);
        }
    }
}
""", 9)

# 395 CS0184 — 절대 참이 될 수 없는 is 검사를 했다.
ep('CS0184', 'SaveSlot.cs',
   "The given expression is never of the provided type 'string'", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    public int score = 1200;

    void Start()
    {
        if (score is string)
        {
            Debug.Log(score);
        }
    }
}
""", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    public int score = 1200;

    void Start()
    {
        if (score is int)
        {
            Debug.Log(score);
        }
    }
}
""", 9)

# 396 CS0458 — null 을 더해 결과가 항상 null 이 됐다.
ep('CS0458', 'SaveSlot.cs',
   "The result of the expression is always null of type 'int?'", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        int? saved = null;
        int? total = saved + null;
        Debug.Log(total);
    }
}
""", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        int? saved = null;
        int? total = saved + 1;
        Debug.Log(total);
    }
}
""", 8)

# 397 CS0464 — null 과 크기를 비교했다.
ep('CS0464', 'SaveSlot.cs',
   "Comparing with null of type 'int?' always produces false", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        int? saved = null;
        if (saved > null)
        {
            Debug.Log(saved);
        }
    }
}
""", """
using UnityEngine;

public class SaveSlot : MonoBehaviour
{
    void Start()
    {
        int? saved = null;
        if (saved > 0)
        {
            Debug.Log(saved);
        }
    }
}
""", 8)

# 398 CS0168 — 선언만 하고 안 쓴 변수가 남았다.
ep('CS0168', 'Combat.cs',
   "The variable 'damage' is declared but never used", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    public int power = 10;

    void Start()
    {
        int damage;
        Debug.Log(power);
    }
}
""", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    public int power = 10;

    void Start()
    {

        Debug.Log(power);
    }
}
""", 9)

# 399 CS0169 — 쓰지 않는 필드가 남았다.
ep('CS0169', 'Player.cs', "The field 'Player.hp' is never used", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp;
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

    public int mana = 50;

    void Start()
    {
        Debug.Log(mana);
    }
}
""", 5)

# 400 CS0219 — 값을 넣어놓고 쓰지 않았다.
ep('CS0219', 'Combat.cs',
   "The variable 'damage' is assigned but its value is never used", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    public int power = 10;

    void Start()
    {
        int damage = 5;
        Debug.Log(power);
    }
}
""", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    public int power = 10;

    void Start()
    {
        int damage = 5;
        Debug.Log(damage);
    }
}
""", 10)

# 401 CS0414 — 필드에 값을 넣어놓고 쓰지 않았다.
ep('CS0414', 'Player.cs',
   "The field 'Player.hp' is assigned but its value is never used", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp = 100;
    public int mana = 50;

    public int GetMana()
    {
        return mana;
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp = 100;
    public int mana = 50;

    public int GetMana()
    {
        return mana + hp;
    }
}
""", 10)

# 402 CS0649 — 값을 한 번도 안 넣은 필드를 읽는다.
ep('CS0649', 'Player.cs',
   "Field 'Player.hp' is never assigned to, and will always have its default value", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp;
    public int mana = 50;

    public int GetHp()
    {
        return hp;
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp = 100;
    public int mana = 50;

    public int GetHp()
    {
        return hp;
    }
}
""", 5)

if __name__ == '__main__':
    write(E, 'tier6.json')
