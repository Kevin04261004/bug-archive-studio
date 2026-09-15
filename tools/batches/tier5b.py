# -*- coding: utf-8 -*-
"""확장 메서드·람다·식 트리·LINQ·async·이터레이터."""
from _common import make, write

E = {}
ep = make(E)

# 319 CS1109 — 확장 메서드를 중첩 클래스에 뒀다.
ep('CS1109', 'Utils.cs',
   "Extension methods must be defined in a top level static class", """
using UnityEngine;

public class Utils : MonoBehaviour
{
    static class MathTools
    {
        static void Twice(this int hp)
        {
        }
    }

    void Start()
    {
        Debug.Log(5);
    }
}
""", """
using UnityEngine;

public class Utils : MonoBehaviour
{
    static class MathTools
    {
        static void Twice(int hp)
        {
        }
    }

    void Start()
    {
        Debug.Log(5);
    }
}
""", 7)

# 320 CS1100 — this 를 두 번째 매개변수에 붙였다.
ep('CS1100', 'MathTools.cs',
   "Method 'Mix' has a parameter modifier 'this' which is not on the first parameter", """
using UnityEngine;

public static class MathTools
{
    static void Mix(int max, this int hp)
    {
        Debug.Log(hp + max);
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(5);
    }
}
""", """
using UnityEngine;

public static class MathTools
{
    static void Mix(this int hp, int max)
    {
        Debug.Log(hp + max);
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(5);
    }
}
""", 5)

# 321 CS1103 — 확장 대상 타입을 dynamic 으로 적었다.
ep('CS1103', 'MathTools.cs',
   "The first parameter of an extension method cannot be of type 'dynamic'", """
using UnityEngine;

public static class MathTools
{
    static void Twice(this dynamic raw)
    {
        Debug.Log(raw);
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(5);
    }
}
""", """
using UnityEngine;

public static class MathTools
{
    static void Twice(this object raw)
    {
        Debug.Log(raw);
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(5);
    }
}
""", 5)

# 322 CS1104 — this 와 params 를 같이 붙였다.
ep('CS1104', 'MathTools.cs',
   "A parameter array cannot be used with the 'this' modifier on an extension method", """
using UnityEngine;

public static class MathTools
{
    static void Add(this params int[] hp)
    {
        Debug.Log(hp.Length);
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(5);
    }
}
""", """
using UnityEngine;

public static class MathTools
{
    static void Add(this int[] hp)
    {
        Debug.Log(hp.Length);
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(5);
    }
}
""", 5)

# 323 CS1113 — 값 타입 확장 메서드로 델리게이트를 만들려 했다.
ep('CS1113', 'Bag.cs',
   "Extension method 'TagTools.Log(Tag)' on value type 'Tag' cannot create delegates", """
using System;
using UnityEngine;
public struct Tag
{
    public int id;
}
public static class TagTools
{
    public static void Log(this Tag tag)
    {
    }
}
public class Bag : MonoBehaviour
{
    void Start()
    {
        Tag tag = new Tag();
        Action show = tag.Log;
    }
}
""", """
using System;
using UnityEngine;
public struct Tag
{
    public int id;
}
public static class TagTools
{
    public static void Log(this Tag tag)
    {
    }
}
public class Bag : MonoBehaviour
{
    void Start()
    {
        Tag tag = new Tag();
        Action show = () => tag.Log();
    }
}
""", 18)

# 324 CS1929 — 확장 메서드가 받는 타입과 다른 값에 불렀다.
ep('CS1929', 'Game.cs',
   "The extension method 'TextTools.Log' requires a receiver of type 'string'", """
using UnityEngine;

public static class TextTools
{
    public static void Log(
        this string text)
    {
        Debug.Log(text);
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        int score = 1;
        score.Log();
    }
}
""", """
using UnityEngine;

public static class TextTools
{
    public static void Log(
        this string text)
    {
        Debug.Log(text);
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        string score = "1";
        score.Log();
    }
}
""", 16)

# 325 CS0748 — 람다 매개변수 중 하나에만 타입을 적었다.
ep('CS0748', 'Combat.cs',
   "Inconsistent lambda parameter usage; parameter types must be all explicit", """
using System;
using UnityEngine;

public class Combat : MonoBehaviour
{
    void Start()
    {
        Func<int, int, int> add =
            (int hp, up) => hp + up;
        Debug.Log(add(1, 2));
    }
}
""", """
using System;
using UnityEngine;

public class Combat : MonoBehaviour
{
    void Start()
    {
        Func<int, int, int> add =
            (hp, up) => hp + up;
        Debug.Log(add(1, 2));
    }
}
""", 9)

# 326 CS1660 — 람다를 델리게이트가 아닌 타입에 넣었다.
ep('CS1660', 'Combat.cs',
   "Cannot convert lambda expression to type 'int'; it is not a delegate type", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    void Start()
    {
        int power = () => 1;
        Debug.Log(power);
    }
}
""", """
using UnityEngine;

public class Combat : MonoBehaviour
{
    void Start()
    {
        int power = 1;
        Debug.Log(power);
    }
}
""", 7)

# 327 CS1661 — 람다 매개변수 타입이 델리게이트와 다르다.
ep('CS1661', 'Watcher.cs',
   "Cannot convert lambda to 'Action<int>'; the parameter types do not match", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    void Start()
    {
        Action<int> onHit =
            (string name) => { };
        onHit(1);
    }
}
""", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    void Start()
    {
        Action<int> onHit =
            (int amount) => { };
        onHit(1);
    }
}
""", 9)

# 328 CS1662 — 람다가 돌려주는 타입이 다르다.
ep('CS1662', 'Score.cs',
   "Cannot convert lambda expression; the return type is not implicitly convertible", """
using System;
using UnityEngine;

public class Score : MonoBehaviour
{
    void Start()
    {
        Func<int> best = () => "1200";
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
        Func<int> best = () => 1200;
        Debug.Log(best());
    }
}
""", 8)

# 329 CS1673 — 구조체 안 람다가 필드를 바로 잡았다.
ep('CS1673', 'Slot.cs',
   "Lambda expressions inside structs cannot access instance members of 'this'", """
using System;
using UnityEngine;

public struct Slot
{
    public int id;

    public void Show()
    {
        int copy = id;
        Action show = () =>
            Debug.Log(id);
    }
}
""", """
using System;
using UnityEngine;

public struct Slot
{
    public int id;

    public void Show()
    {
        int copy = id;
        Action show = () =>
            Debug.Log(copy);
    }
}
""", 12)

# 330 CS0834 — 식 트리에 블록 본문 람다를 넣었다.
ep('CS0834', 'Query.cs',
   "A lambda expression with a statement body cannot be converted to an expression tree", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Query : MonoBehaviour
{
    void Start()
    {
        Expression<Func<int>> best =
            () => { return 1200; };
        Debug.Log(best);
    }
}
""", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Query : MonoBehaviour
{
    void Start()
    {
        Expression<Func<int>> best =
            () => 1200;
        Debug.Log(best);
    }
}
""", 10)

# 331 CS0832 — 식 트리에 대입을 넣었다.
ep('CS0832', 'Query.cs',
   "An expression tree may not contain an assignment operator", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Query : MonoBehaviour
{
    void Start()
    {
        int score = 0;
        Expression<Func<int>> best =
            () => score = 1200;
        Debug.Log(best);
    }
}
""", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Query : MonoBehaviour
{
    void Start()
    {
        int score = 0;
        Expression<Func<int>> best =
            () => score + 1200;
        Debug.Log(best);
    }
}
""", 11)

# 332 CS0831 — 식 트리에 base 접근을 넣었다.
ep('CS0831', 'Boss.cs',
   "An expression tree may not contain a base access", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Enemy
{
    public int hp = 100;
}

public class Boss : Enemy
{
    void Show()
    {
        Expression<Func<int>> get =
            () => base.hp;
        Debug.Log(get);
    }
}
""", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Enemy
{
    public int hp = 100;
}

public class Boss : Enemy
{
    void Show()
    {
        Expression<Func<int>> get =
            () => hp;
        Debug.Log(get);
    }
}
""", 15)

# 333 CS0845 — 식 트리의 ?? 왼쪽이 null 이다.
ep('CS0845', 'Query.cs',
   "An expression tree lambda may not contain a coalescing operator with a null left side", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Query : MonoBehaviour
{
    void Start()
    {
        Expression<Func<int>> best =
            () => null ?? 1200;
        Debug.Log(best);
    }
}
""", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Query : MonoBehaviour
{
    void Start()
    {
        Expression<Func<int>> best =
            () => 1200;
        Debug.Log(best);
    }
}
""", 10)

# 334 CS0853 — 식 트리에 이름 붙인 인자를 썼다.
ep('CS0853', 'Query.cs',
   "An expression tree may not contain a named argument specification", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Query : MonoBehaviour
{
    int Add(int left, int right)
    {
        return left + right;
    }

    void Start()
    {
        Expression<Func<int>> sum =
            () => Add(left: 1, right: 2);
        Debug.Log(sum);
    }
}
""", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Query : MonoBehaviour
{
    int Add(int left, int right)
    {
        return left + right;
    }

    void Start()
    {
        Expression<Func<int>> sum =
            () => Add(1, 2);
        Debug.Log(sum);
    }
}
""", 15)

# 335 CS0854 — 식 트리에서 선택적 인자를 생략했다.
ep('CS0854', 'Query.cs',
   "An expression tree may not contain a call that uses optional arguments", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Query : MonoBehaviour
{
    int Add(int left, int right = 2)
    {
        return left + right;
    }

    void Start()
    {
        Expression<Func<int>> sum =
            () => Add(1);
        Debug.Log(sum);
    }
}
""", """
using System;
using System.Linq.Expressions;
using UnityEngine;

public class Query : MonoBehaviour
{
    int Add(int left, int right = 2)
    {
        return left + right;
    }

    void Start()
    {
        Expression<Func<int>> sum =
            () => Add(1, 2);
        Debug.Log(sum);
    }
}
""", 15)

# 336 CS0837 — is 왼쪽에 람다를 뒀다.
ep('CS0837', 'Watcher.cs',
   "The first operand of an 'is' or 'as' operator may not be a lambda expression", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    void Start()
    {
        Func<int> get = () => 1;
        bool ok = (() => 1) is Func<int>;
        Debug.Log(ok);
    }
}
""", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    void Start()
    {
        Func<int> get = () => 1;
        bool ok = get is Func<int>;
        Debug.Log(ok);
    }
}
""", 9)

# 337 CS1632 — 람다 안에서 바깥 반복문을 끊으려 했다.
ep('CS1632', 'Spawner.cs',
   "Control cannot leave the body of an anonymous method or lambda expression", """
using System;
using UnityEngine;

public class Spawner : MonoBehaviour
{
    void Start()
    {
        for (int i = 0; i < 3; i++)
        {
            Action go = () => { break; };
            go();
        }
    }
}
""", """
using System;
using UnityEngine;

public class Spawner : MonoBehaviour
{
    void Start()
    {
        for (int i = 0; i < 3; i++)
        {
            Action go = () => { return; };
            go();
        }
    }
}
""", 10)

# 338 CS1628 — 람다가 ref 매개변수를 잡았다.
ep('CS1628', 'Health.cs',
   "Cannot use ref or out parameter 'hp' inside a lambda expression", """
using System;
using UnityEngine;

public class Health : MonoBehaviour
{
    void Bump(ref int hp)
    {
        int copy = hp;
        Action log = () =>
            Debug.Log(hp);
        log();
    }
}
""", """
using System;
using UnityEngine;

public class Health : MonoBehaviour
{
    void Bump(ref int hp)
    {
        int copy = hp;
        Action log = () =>
            Debug.Log(copy);
        log();
    }
}
""", 10)

# 339 CS1688 — out 매개변수가 있는 델리게이트에 매개변수 목록 없는 익명 메서드를 넣었다.
ep('CS1688', 'Watcher.cs',
   "Cannot convert anonymous method without a parameter list; it has out parameters", """
using UnityEngine;

public delegate void Handler(out int id);

public class Watcher : MonoBehaviour
{
    void Start()
    {
        Handler read =
            delegate { };
        Debug.Log(read);
    }
}
""", """
using UnityEngine;

public delegate void Handler(out int id);

public class Watcher : MonoBehaviour
{
    void Start()
    {
        Handler read =
            (out int id) => id = 1;
        Debug.Log(read);
    }
}
""", 10)

# 340 CS0742 — 쿼리를 select 없이 끝냈다.
ep('CS0742', 'Inventory.cs',
   "A query body must end with a select clause or a group clause", """
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    List<int> prices = new();

    void Start()
    {
        var cheap = from price in prices
                    where price < 100;
        Debug.Log(cheap);
    }
}
""", """
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    List<int> prices = new();

    void Start()
    {
        var cheap = from price in prices
                    select price;
        Debug.Log(cheap);
    }
}
""", 12)

# 341 CS0743 — join 에 on 을 빠뜨렸다.
ep('CS0743', 'Shop.cs', "Expected contextual keyword 'on'", """
using System.Linq;
using UnityEngine;

public class Shop : MonoBehaviour
{
    int[] ids = new int[2];
    int[] owned = new int[2];

    void Start()
    {
        var rows = from id in ids
                join own in owned
                    id equals own
                select id;
    }
}
""", """
using System.Linq;
using UnityEngine;

public class Shop : MonoBehaviour
{
    int[] ids = new int[2];
    int[] owned = new int[2];

    void Start()
    {
        var rows = from id in ids
                join own in owned
                    on id equals own
                select id;
    }
}
""", 13)

# 342 CS0744 — join 에 == 를 썼다.
ep('CS0744', 'Shop.cs', "Expected contextual keyword 'equals'", """
using System.Linq;
using UnityEngine;

public class Shop : MonoBehaviour
{
    int[] ids = new int[2];
    int[] owned = new int[2];

    void Start()
    {
        var rows = from id in ids
                join own in owned
                    on id == own
                select id;
    }
}
""", """
using System.Linq;
using UnityEngine;

public class Shop : MonoBehaviour
{
    int[] ids = new int[2];
    int[] owned = new int[2];

    void Start()
    {
        var rows = from id in ids
                join own in owned
                    on id equals own
                select id;
    }
}
""", 13)

# 343 CS0745 — group 에 by 를 빠뜨렸다.
ep('CS0745', 'Shop.cs', "Expected contextual keyword 'by'", """
using System.Linq;
using UnityEngine;

public class Shop : MonoBehaviour
{
    int[] ids = new int[4];

    void Start()
    {
        var rows = from id in ids
                group id id;
        Debug.Log(rows);
    }
}
""", """
using System.Linq;
using UnityEngine;

public class Shop : MonoBehaviour
{
    int[] ids = new int[4];

    void Start()
    {
        var rows = from id in ids
                group id by id;
        Debug.Log(rows);
    }
}
""", 11)

# 344 CS0746 — 익명 타입에 이름 없는 값을 넣었다.
ep('CS0746', 'Report.cs',
   "Invalid anonymous type member declarator; use a member assignment", """
using UnityEngine;

public class Report : MonoBehaviour
{
    public int score = 120;

    void Start()
    {
        var row = new { score, 1 };
        Debug.Log(row);
    }
}
""", """
using UnityEngine;

public class Report : MonoBehaviour
{
    public int score = 120;

    void Start()
    {
        var row = new { score, id = 1 };
        Debug.Log(row);
    }
}
""", 9)

# 345 CS0747 — 객체 초기화에 이름 없는 값을 넣었다.
ep('CS0747', 'Game.cs', "Invalid initializer member declarator", """
using UnityEngine;

public class Player
{
    public int hp;
}

public class Game : MonoBehaviour
{
    void Start()
    {
        var one = new Player { 100 };
        Debug.Log(one.hp);
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
        var one = new Player { hp = 100 };
        Debug.Log(one.hp);
    }
}
""", 12)

# 346 CS1063 — Add 가 없는 타입에 컬렉션 초기화를 썼다.
ep('CS1063', 'Game.cs',
   "Cannot initialize 'Bag' with a collection initializer; no suitable Add method", """
using System.Collections;
using UnityEngine;

public class Bag : IEnumerable
{
    public IEnumerator GetEnumerator()
    {
        yield break;
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        var bag = new Bag { 1 };
        Debug.Log(bag);
    }
}
""", """
using System.Collections;
using UnityEngine;

public class Bag : IEnumerable
{
    public IEnumerator GetEnumerator()
    {
        yield break;
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        var bag = new Bag();
        Debug.Log(bag);
    }
}
""", 16)

# 347 CS1065 — 람다 매개변수에 기본값을 줬다.
ep('CS1065', 'Watcher.cs', "Default values are not valid in this context", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    void Start()
    {
        Action<int> onHit =
            (int amount = 1) => { };
        onHit(2);
    }
}
""", """
using System;
using UnityEngine;

public class Watcher : MonoBehaviour
{
    void Start()
    {
        Action<int> onHit =
            (int amount) => { };
        onHit(2);
    }
}
""", 9)

# 348 CS4032 — 값을 돌려주는 메서드에 async 를 안 붙였다.
ep('CS4032', 'Loader.cs',
   "The 'await' operator can only be used within an async method", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    int Load()
    {
        await Task.Delay(1);
        return 1;
    }
}
""", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    async Task<int> Load()
    {
        await Task.Delay(1);
        return 1;
    }
}
""", 6)

# 349 CS4033 — void 메서드에 async 를 안 붙였다.
ep('CS4033', 'Loader.cs',
   "The 'await' operator can only be used within an async method", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    void Load()
    {
        await Task.Delay(1);
        Debug.Log("loaded");
    }

    void Start()
    {
        Load();
    }
}
""", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    async Task Load()
    {
        await Task.Delay(1);
        Debug.Log("loaded");
    }

    void Start()
    {
        Load();
    }
}
""", 6)

# 350 CS4008 — void 를 await 했다.
ep('CS4008', 'Loader.cs', "Cannot await 'void'", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    void Ping() { }

    async Task Load()
    {
        await Ping();
        Debug.Log("done");
    }
}
""", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    Task Ping() => Task.CompletedTask;

    async Task Load()
    {
        await Ping();
        Debug.Log("done");
    }
}
""", 6)

# 351 CS4009 — 진입점을 async void 로 만들었다.
ep('CS4009', 'Program.cs',
   "A void or int returning entry point cannot be async", """
using System;
using System.Threading.Tasks;

public class Program
{
    static async void Main()
    {
        await Task.Delay(1);
        Console.WriteLine("done");
    }
}
""", """
using System;
using System.Threading.Tasks;

public class Program
{
    static async Task Main()
    {
        await Task.Delay(1);
        Console.WriteLine("done");
    }
}
""", 6)

# 352 CS1994 — 본문 없는 메서드에 async 를 붙였다.
ep('CS1994', 'Loader.cs',
   "The async modifier can only be used in methods that have a body", """
using System.Threading.Tasks;
using UnityEngine;

public abstract class Loader
{
    public abstract async Task Go();

    public void Ready()
    {
        Debug.Log("ready");
    }
}
""", """
using System.Threading.Tasks;
using UnityEngine;

public abstract class Loader
{
    public abstract Task Go();

    public void Ready()
    {
        Debug.Log("ready");
    }
}
""", 6)

# 353 CS1996 — lock 안에서 await 했다.
ep('CS1996', 'Loader.cs',
   "Cannot await in the body of a lock statement", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    async Task Load()
    {
        lock (this)
        {
            await Task.Delay(1);
        }
        Debug.Log("done");
    }
}
""", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    async Task Load()
    {
        lock (this)
        {
            Debug.Log("locked");
        }
        Debug.Log("done");
    }
}
""", 10)

# 354 CS1998 — async 인데 await 가 없다.
ep('CS1998', 'Loader.cs',
   "This async method lacks await operators and will run synchronously", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    async Task<int> Load()
    {

        return 1;
    }

    void Start()
    {
        Load();
    }
}
""", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    async Task<int> Load()
    {
        await Task.Delay(1);
        return 1;
    }

    void Start()
    {
        Load();
    }
}
""", 8)

# 355 CS4014 — Task 를 await 하지 않고 버렸다.
ep('CS4014', 'Loader.cs',
   "Because this call is not awaited, execution continues before the call completes", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    async Task Load()
    {
        Task.Delay(1);
        Debug.Log("done");
    }
}
""", """
using System.Threading.Tasks;
using UnityEngine;

public class Loader : MonoBehaviour
{
    async Task Load()
    {
        await Task.Delay(1);
        Debug.Log("done");
    }
}
""", 8)

# 356 CS1621 — 람다 안에서 yield 했다.
ep('CS1621', 'Waves.cs',
   "The yield statement cannot be used inside a lambda expression", """
using System;
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts()
    {
        Action go = () =>
        {
            yield return 1;
        };
        yield return 2;
    }
}
""", """
using System;
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts()
    {
        Action go = () =>
        {
            return;
        };
        yield return 2;
    }
}
""", 11)

# 357 CS1622 — 이터레이터에서 값을 return 했다.
ep('CS1622', 'Waves.cs',
   "Cannot return a value from an iterator; use the yield return statement", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts()
    {
        yield return 1;
        yield return 2;
        return 3;
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

# 358 CS1623 — 이터레이터에 ref 매개변수를 뒀다.
ep('CS1623', 'Waves.cs',
   "Iterators cannot have ref, in or out parameters", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts(ref int start)
    {
        yield return start;
        yield return start + 1;
    }
}
""", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    IEnumerable<int> Counts(int start)
    {
        yield return start;
        yield return start + 1;
    }
}
""", 6)

# 359 CS1624 — 반환형이 이터레이터 타입이 아니다.
ep('CS1624', 'Waves.cs',
   "The body of 'Counts()' cannot be an iterator block because 'int' is not an iterator type", """
using System.Collections.Generic;
using UnityEngine;

public class Waves : MonoBehaviour
{
    int Counts()
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

# 360 CS1625 — finally 안에서 yield 했다.
ep('CS1625', 'Waves.cs', "Cannot yield in the body of a finally clause", """
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
        finally
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
        finally
        {
            Debug.Log("done");
        }
    }
}
""", 15)

if __name__ == '__main__':
    write(E, 'tier5b.json')
