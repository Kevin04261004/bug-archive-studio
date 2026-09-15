# -*- coding: utf-8 -*-
"""5티어 앞부분: 제네릭과 제약 조건. 오브젝트 풀·캐시 같은 실제 제네릭 코드를 무대로."""
from _common import make, write

E = {}
ep = make(E)

# 277 CS0305 — 제네릭 타입에 인자를 안 적었다.
ep('CS0305', 'Spawner.cs',
   "Using the generic type 'Pool<T>' requires 1 type arguments", """
using UnityEngine;

public class Pool<T>
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    void Start()
    {
        Pool bullets = new Pool<int>();
        Debug.Log(bullets.item);
    }
}
""", """
using UnityEngine;

public class Pool<T>
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    void Start()
    {
        var bullets = new Pool<int>();
        Debug.Log(bullets.item);
    }
}
""", 12)

# 278 CS0307 — 변수에 타입 인자를 붙였다.
ep('CS0307', 'Spawner.cs',
   "The variable 'count' cannot be used with type arguments", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public int total = 5;

    void Start()
    {
        int count = total;
        Debug.Log(count<int>);
    }
}
""", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public int total = 5;

    void Start()
    {
        int count = total;
        Debug.Log(count);
    }
}
""", 10)

# 279 CS0308 — 제네릭이 아닌 메서드에 타입 인자를 붙였다.
ep('CS0308', 'Spawner.cs',
   "The non-generic method 'Spawner.Show()' cannot be used with type arguments", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    void Show() { }

    void Start()
    {
        Show<int>();
        Debug.Log("shown");
    }
}
""", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    void Show() { }

    void Start()
    {
        Show();
        Debug.Log("shown");
    }
}
""", 9)

# 280 CS0310 — 매개변수 없는 생성자가 필요한데 없다.
ep('CS0310', 'Spawner.cs',
   "'Bullet' must be a non-abstract type with a public parameterless constructor", """
using UnityEngine;

public class Bullet
{
    public Bullet(int speed) { }
}

public class Pool<T> where T : new()
{
    public T Make() => new T();
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}
""", """
using UnityEngine;

public class Bullet
{
    public Bullet() { }
}

public class Pool<T> where T : new()
{
    public T Make() => new T();
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}
""", 5)

# 281 CS0311 — 제약이 요구하는 타입과 관계가 없다.
ep('CS0311', 'Spawner.cs',
   "There is no implicit reference conversion from 'string' to 'Unit'", """
using UnityEngine;

public class Unit
{
    public int hp;
}

public class Pool<T>
    where T : Unit
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<string> pool = new();
}
""", """
using UnityEngine;

public class Unit
{
    public int hp;
}

public class Pool<T>
    where T : Unit
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<Unit> pool = new();
}
""", 16)

# 282 CS0312 — T 가 U 로 변환되지 않는다.
ep('CS0312', 'Spawner.cs',
   "There is no boxing conversion or type parameter conversion from 'int' to 'U'", """
using UnityEngine;

public class Pool<T, U> where T : U
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<int, string> pool = new();

    void Start()
    {
        Debug.Log(pool.item);
    }
}
""", """
using UnityEngine;

public class Pool<T, U> where T : U
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<string, object> pool = new();

    void Start()
    {
        Debug.Log(pool.item);
    }
}
""", 10)

# 283 CS0313 — nullable 로 감싸면 제약을 못 채운다.
ep('CS0313', 'Runner.cs',
   "The nullable type 'Timer?' does not satisfy the constraint 'ITick'", """
using UnityEngine;

public interface ITick
{
    void Tick();
}

public struct Timer : ITick
{
    public void Tick() { }
}
public class Pool<T> where T : ITick
{
    public T item;
}

public class Runner : MonoBehaviour
{
    Pool<Timer?> pool = new();
}
""", """
using UnityEngine;

public interface ITick
{
    void Tick();
}

public struct Timer : ITick
{
    public void Tick() { }
}
public class Pool<T> where T : ITick
{
    public T item;
}

public class Runner : MonoBehaviour
{
    Pool<Timer> pool = new();
}
""", 19)

# 284 CS0314 — 바깥 제네릭에 같은 제약을 안 달았다.
ep('CS0314', 'Bag.cs',
   "There is no boxing conversion or type parameter conversion from 'T' to 'Unit'", """
using UnityEngine;

public class Unit
{
    public int hp;
}

public class Pool<T> where T : Unit
{
    public T item;
}
public class Bag<T>
{
    Pool<T> pool;

    public void Log()
    {
        Debug.Log(pool);
    }
}
""", """
using UnityEngine;

public class Unit
{
    public int hp;
}

public class Pool<T> where T : Unit
{
    public T item;
}
public class Bag<T> where T : Unit
{
    Pool<T> pool;

    public void Log()
    {
        Debug.Log(pool);
    }
}
""", 12)

# 285 CS0315 — 값 타입은 참조 제약을 못 채운다.
ep('CS0315', 'Spawner.cs',
   "There is no boxing conversion from 'int' to 'Enemy'", """
using UnityEngine;

public class Enemy
{
    public int hp;
}

public class Pool<T> where T : Enemy
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<int> pool = new();
}
""", """
using UnityEngine;

public class Enemy
{
    public int hp;
}

public class Pool<T> where T : Enemy
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<Enemy> pool = new();
}
""", 15)

# 286 CS0452 — class 제약에 값 타입을 넣었다.
ep('CS0452', 'Spawner.cs',
   "The type 'int' must be a reference type in order to use it as parameter 'T'", """
using UnityEngine;

public class Pool<T> where T : class
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<int> pool = new();

    void Start()
    {
        Debug.Log(pool.item);
    }
}
""", """
using UnityEngine;

public class Pool<T> where T : class
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<string> pool = new();

    void Start()
    {
        Debug.Log(pool.item);
    }
}
""", 10)

# 287 CS0453 — struct 제약에 참조 타입을 넣었다.
ep('CS0453', 'Spawner.cs',
   "The type 'string' must be a non-nullable value type to use it as parameter 'T'", """
using UnityEngine;

public class Pool<T> where T : struct
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<string> pool = new();

    void Start()
    {
        Debug.Log(pool.item);
    }
}
""", """
using UnityEngine;

public class Pool<T> where T : struct
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<int> pool = new();

    void Start()
    {
        Debug.Log(pool.item);
    }
}
""", 10)

# 288 CS0304 — new() 제약 없이 T 를 만들었다.
ep('CS0304', 'Pool.cs',
   "Cannot create an instance of 'T' because it does not have the new() constraint", """
using UnityEngine;

public class Pool<T>
{
    public T Make()
    {
        return new T();
    }
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}

public class Bullet { }
""", """
using UnityEngine;

public class Pool<T> where T : new()
{
    public T Make()
    {
        return new T();
    }
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}

public class Bullet { }
""", 3)

# 289 CS0403 — T 에 null 을 돌려줬다.
ep('CS0403', 'Pool.cs',
   "Cannot convert null to type parameter 'T'; it could be a non-nullable value type", """
using UnityEngine;

public class Pool<T>
{
    public T Get()
    {
        return null;
    }
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}

public class Bullet { }
""", """
using UnityEngine;

public class Pool<T>
{
    public T Get()
    {
        return default;
    }
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}

public class Bullet { }
""", 7)

# 290 CS0413 — 제약 없는 T 에 as 를 썼다.
ep('CS0413', 'Pool.cs',
   "The type parameter 'T' cannot be used with 'as'; it has no class type constraint", """
using UnityEngine;

public class Pool<T>
{
    public T Cast(object raw)
    {
        return raw as T;
    }
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}

public class Bullet { }
""", """
using UnityEngine;

public class Pool<T> where T : class
{
    public T Cast(object raw)
    {
        return raw as T;
    }
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}

public class Bullet { }
""", 3)

# 291 CS0411 — 인자가 없어 타입을 추론할 수 없다.
ep('CS0411', 'Spawner.cs',
   "The type arguments for method 'Make<T>()' cannot be inferred from the usage", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    T Make<T>()
    {
        return default;
    }

    void Start()
    {
        var made = Make();
        Debug.Log(made);
    }
}
""", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    T Make<T>()
    {
        return default;
    }

    void Start()
    {
        var made = Make<int>();
        Debug.Log(made);
    }
}
""", 12)

# 292 CS0401 — new() 를 맨 뒤에 안 뒀다.
ep('CS0401', 'Pool.cs',
   "The new() constraint must be the last constraint specified", """
using UnityEngine;

public class Pool<T>
    where T : new(), class
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}

public class Bullet { }
""", """
using UnityEngine;

public class Pool<T>
    where T : class, new()
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}

public class Bullet { }
""", 4)

# 293 CS0405 — 같은 제약을 두 번 적었다.
ep('CS0405', 'Pool.cs',
   "Duplicate constraint 'class' for type parameter 'T'", """
using UnityEngine;

public class Pool<T>
    where T : class, class
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}

public class Bullet { }
""", """
using UnityEngine;

public class Pool<T>
    where T : class, new()
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<Bullet> pool = new();
}

public class Bullet { }
""", 4)

# 294 CS0406 — 클래스 제약을 인터페이스 뒤에 뒀다.
ep('CS0406', 'Pool.cs',
   "The class type constraint 'Unit' must come before any other constraints", """
using UnityEngine;

public interface ITick
{
    void Tick();
}

public class Unit { }

public class Pool<T>
    where T : ITick, Unit
{
    public T item;
}
""", """
using UnityEngine;

public interface ITick
{
    void Tick();
}

public class Unit { }

public class Pool<T>
    where T : Unit, ITick
{
    public T item;
}
""", 11)

# 295 CS0409 — 같은 타입 매개변수에 where 를 두 번 썼다.
ep('CS0409', 'Cache.cs',
   "A constraint clause has already been specified for type parameter 'K'", """
using UnityEngine;

public class Cache<K, V>
    where K : class
    where K : new()
{
    public K key;
    public V value;
}

public class Store : MonoBehaviour
{
    Cache<string, int> cache = new();
}
""", """
using UnityEngine;

public class Cache<K, V>
    where K : class
    where V : new()
{
    public K key;
    public V value;
}

public class Store : MonoBehaviour
{
    Cache<string, int> cache = new();
}
""", 5)

# 296 CS0449 — class 제약을 인터페이스 뒤에 뒀다.
ep('CS0449', 'Pool.cs',
   "The class or struct constraint must come before any other constraints", """
using UnityEngine;

public interface ITick
{
    void Tick();
}

public class Pool<T>
    where T : ITick, class
{
    public T item;
}
""", """
using UnityEngine;

public interface ITick
{
    void Tick();
}

public class Pool<T>
    where T : class, ITick
{
    public T item;
}
""", 9)

# 297 CS0450 — class 제약과 클래스 제약을 같이 적었다.
ep('CS0450', 'Pool.cs',
   "'Unit': cannot specify both a constraint class and the class or struct constraint", """
using UnityEngine;

public class Unit { }

public class Pool<T>
    where T : class, Unit
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<Unit> pool = new();
}
""", """
using UnityEngine;

public class Unit { }

public class Pool<T>
    where T : Unit
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<Unit> pool = new();
}
""", 6)

# 298 CS0451 — struct 제약에 new() 를 붙였다.
ep('CS0451', 'Box.cs',
   "The new() constraint cannot be used with the struct constraint", """
using UnityEngine;

public class Box<T>
    where T : struct, new()
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Box<int> box = new();

    void Start()
    {
        Debug.Log(box.item);
    }
}
""", """
using UnityEngine;

public class Box<T>
    where T : struct
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Box<int> box = new();

    void Start()
    {
        Debug.Log(box.item);
    }
}
""", 4)

# 299 CS0454 — 두 제약이 서로를 가리킨다.
ep('CS0454', 'Cache.cs',
   "Circular constraint dependency involving 'K' and 'V'", """
using UnityEngine;

public class Cache<K, V>
    where K : V
    where V : K
{
    public K key;
    public V value;
}

public class Store : MonoBehaviour
{
    Cache<string, object> cache = new();
}
""", """
using UnityEngine;

public class Cache<K, V>
    where K : V
    where V : class
{
    public K key;
    public V value;
}

public class Store : MonoBehaviour
{
    Cache<string, object> cache = new();
}
""", 5)

# 300 CS0455 — 상속받은 제약끼리 부딪힌다.
ep('CS0455', 'Cache.cs',
   "Type parameter 'K' inherits conflicting constraints 'struct' and 'class'", """
using UnityEngine;

public class Cache<K, V>
    where K : class, V
    where V : struct
{
    public K key;
    public V value;
}

public class Store : MonoBehaviour
{
    Cache<string, int> cache = new();
}
""", """
using UnityEngine;

public class Cache<K, V>
    where K : class, V
    where V : class
{
    public K key;
    public V value;
}

public class Store : MonoBehaviour
{
    Cache<string, int> cache = new();
}
""", 5)

# 301 CS0456 — struct 제약이 걸린 매개변수를 제약으로 썼다.
ep('CS0456', 'Cache.cs',
   "Type parameter 'V' has the struct constraint so 'V' cannot be used as a constraint", """
using UnityEngine;

public class Cache<K, V>
    where K : V
    where V : struct
{
    public K key;
    public V value;
}

public class Store : MonoBehaviour
{
    Cache<string, object> cache = new();
}
""", """
using UnityEngine;

public class Cache<K, V>
    where K : V
    where V : class
{
    public K key;
    public V value;
}

public class Store : MonoBehaviour
{
    Cache<string, object> cache = new();
}
""", 5)

# 302 CS0425 — 명시적 구현의 제약이 인터페이스와 다르다.
ep('CS0425', 'Boss.cs',
   "The constraints for type parameter 'T' of 'Boss.Hit<T>()' must match the interface", """
using UnityEngine;

public interface IHitter
{
    void Hit<T>() where T : class;
}

public class Boss : IHitter
{
    void IHitter.Hit<T>()
        where T : struct
    { }
}
""", """
using UnityEngine;

public interface IHitter
{
    void Hit<T>() where T : class;
}

public class Boss : IHitter
{
    void IHitter.Hit<T>()
        where T : class
    { }
}
""", 11)

# 303 CS0460 — override 에 제약을 다시 적었다.
ep('CS0460', 'Boss.cs',
   "Constraints for an override method are inherited from the base method", """
using UnityEngine;

public class Enemy
{
    public virtual void Hit<T>() { }
}

public class Boss : Enemy
{
    public override void Hit<T>()
        where T : class
    { }
}
""", """
using UnityEngine;

public class Enemy
{
    public virtual void Hit<T>() { }
}

public class Boss : Enemy
{
    public override void Hit<T>()

    { }
}
""", 11)

# 304 CS0689 — 타입 매개변수를 상속했다.
ep('CS0689', 'Pool.cs',
   "Cannot derive from 'T' because it is a type parameter", """
using UnityEngine;

public class Unit
{
    public int hp;
}

public class Pool<T> : T
{
    public T item;
}
""", """
using UnityEngine;

public class Unit
{
    public int hp;
}

public class Pool<T> : Unit
{
    public T item;
}
""", 8)

# 305 CS0692 — 타입 매개변수 이름이 겹친다.
ep('CS0692', 'Pair.cs', "Duplicate type parameter 'A'", """
using UnityEngine;

public class Pair<A, B, A>
{
    public A first;
    public B second;
}

public class Store : MonoBehaviour
{
    Pair<int, string, bool> pair;
}
""", """
using UnityEngine;

public class Pair<A, B, C>
{
    public A first;
    public B second;
}

public class Store : MonoBehaviour
{
    Pair<int, string, bool> pair;
}
""", 3)

# 306 CS0694 — 타입 매개변수 이름이 클래스 이름과 같다.
ep('CS0694', 'Pair.cs',
   "Type parameter 'Pair' has the same name as the containing type", """
using UnityEngine;

public class Pair<A, Pair>
{
    public A first;
}

public class Store : MonoBehaviour
{
    Pair<int, string> pair;
}
""", """
using UnityEngine;

public class Pair<A, B>
{
    public A first;
}

public class Store : MonoBehaviour
{
    Pair<int, string> pair;
}
""", 3)

# 307 CS0699 — 없는 타입 매개변수에 제약을 걸었다.
ep('CS0699', 'Cache.cs',
   "'Cache<K, V>' does not define type parameter 'X'", """
using UnityEngine;

public class Cache<K, V>
    where K : class
    where X : new()
{
    public K key;
    public V value;
}

public class Store : MonoBehaviour
{
    Cache<string, int> cache = new();
}
""", """
using UnityEngine;

public class Cache<K, V>
    where K : class
    where V : new()
{
    public K key;
    public V value;
}

public class Store : MonoBehaviour
{
    Cache<string, int> cache = new();
}
""", 5)

# 308 CS0701 — sealed 클래스를 제약으로 썼다.
ep('CS0701', 'Pool.cs',
   "'Unit' is not a valid constraint; a sealed class cannot be used as a constraint", """
using UnityEngine;

public sealed class Unit { }

public class Pool<T>
    where T : Unit
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<Unit> pool = new();
}
""", """
using UnityEngine;

public class Unit { }

public class Pool<T>
    where T : Unit
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<Unit> pool = new();
}
""", 3)

# 309 CS0702 — object 를 제약으로 썼다.
ep('CS0702', 'Pool.cs', "Constraint cannot be special class 'object'", """
using UnityEngine;

public class Pool<T> where T : object
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<int> pool = new();

    void Start()
    {
        Debug.Log(pool.item);
    }
}
""", """
using UnityEngine;

public class Pool<T>
{
    public T item;
}

public class Spawner : MonoBehaviour
{
    Pool<int> pool = new();

    void Start()
    {
        Debug.Log(pool.item);
    }
}
""", 3)

# 310 CS0703 — 제약 타입이 제네릭 클래스보다 좁다.
ep('CS0703', 'Pool.cs',
   "Inconsistent accessibility: constraint type 'Unit' is less accessible", """
using UnityEngine;

class Unit
{
    public int hp;
}

public class Pool<T> where T : Unit
{
    public T item;
}
""", """
using UnityEngine;

public class Unit
{
    public int hp;
}

public class Pool<T> where T : Unit
{
    public T item;
}
""", 3)

# 311 CS0706 — 제약에 값 타입을 적었다.
ep('CS0706', 'Repo.cs',
   "Invalid constraint type 'int'; use an interface, a class or a type parameter", """
using System;
using UnityEngine;

public class Repo<T, K>
    where K : IComparable
    where T : int
{
    public T item;
    public K key;
}

public class Store : MonoBehaviour
{
    Repo<int, int> repo = new();
}
""", """
using System;
using UnityEngine;

public class Repo<T, K>
    where K : IComparable
    where T : IComparable
{
    public T item;
    public K key;
}

public class Store : MonoBehaviour
{
    Repo<int, int> repo = new();
}
""", 6)

# 312 CS0080 — 제네릭이 아닌 클래스에 제약을 달았다.
ep('CS0080', 'Pool.cs',
   "Constraints are not allowed on non-generic declarations", """
using UnityEngine;

public class Pool where T : class
{
    public int count;
}

public class Spawner : MonoBehaviour
{
    Pool pool = new();

    void Start()
    {
        Debug.Log(pool.count);
    }
}
""", """
using UnityEngine;

public class Pool
{
    public int count;
}

public class Spawner : MonoBehaviour
{
    Pool pool = new();

    void Start()
    {
        Debug.Log(pool.count);
    }
}
""", 3)

# 313 CS0081 — 타입 매개변수 자리에 타입을 적었다.
ep('CS0081', 'Pool.cs',
   "Type parameter declaration must be an identifier not a type", """
using UnityEngine;

public class Pool<int>
{
    public int count;
}

public class Spawner : MonoBehaviour
{
    Pool<int> pool = new();

    void Start()
    {
        Debug.Log(pool.count);
    }
}
""", """
using UnityEngine;

public class Pool<T>
{
    public int count;
}

public class Spawner : MonoBehaviour
{
    Pool<int> pool = new();

    void Start()
    {
        Debug.Log(pool.count);
    }
}
""", 3)

# 314 CS0316 — 인덱서 매개변수를 value 라고 지었다.
ep('CS0316', 'Inventory.cs',
   "The parameter name 'value' conflicts with an automatically-generated parameter name", """
using UnityEngine;

public class Inventory : MonoBehaviour
{
    int[] slots = new int[9];

    public int this[int value]
    {
        get { return slots[0]; }
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

    public int this[int index]
    {
        get { return slots[0]; }
    }

    void Start()
    {
        Debug.Log(slots[0]);
    }
}
""", 7)

# 315 CS0412 — 지역 변수 이름이 타입 매개변수와 같다.
ep('CS0412', 'Spawner.cs',
   "'T': a local variable cannot have the same name as a method type parameter", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    void Show<T>()
    {
        int T = 1;
        Debug.Log("shown");
    }

    void Start()
    {
        Show<int>();
    }
}
""", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
    void Show<T>()
    {
        int count = 1;
        Debug.Log("shown");
    }

    void Start()
    {
        Show<int>();
    }
}
""", 7)

# 316 CS0306 — 포인터 타입을 제네릭 인자로 넣었다.
ep('CS0306', 'Pixels.cs',
   "The type 'int*' may not be used as a type argument", """
using System.Collections.Generic;
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        var list = new List<int*>();
        Debug.Log(list.Count);
    }
}
""", """
using System.Collections.Generic;
using UnityEngine;

public class Pixels : MonoBehaviour
{
    unsafe void Scan()
    {
        var list = new List<int>();
        Debug.Log(list.Count);
    }
}
""", 8)

# 317 CS1105 — 확장 메서드에 static 을 안 붙였다.
ep('CS1105', 'MathTools.cs',
   "Extension method 'MathTools.Twice(int)' must be static", """
using UnityEngine;

public static class MathTools
{
    public void Twice(this int hp)
    {
        Debug.Log(hp * 2);
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
    public static void Twice(this int hp)
    {
        Debug.Log(hp * 2);
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

# 318 CS1106 — 확장 메서드를 담은 클래스에 static 을 안 붙였다.
ep('CS1106', 'MathTools.cs',
   "Extension method must be defined in a non-generic static class", """
using UnityEngine;

public class MathTools
{
    public static void Twice(this int hp)
    {
        Debug.Log(hp * 2);
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
    public static void Twice(this int hp)
    {
        Debug.Log(hp * 2);
    }
}

public class Game : MonoBehaviour
{
    void Start()
    {
        Debug.Log(5);
    }
}
""", 3)

if __name__ == '__main__':
    write(E, 'tier5a.json')
