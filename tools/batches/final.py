# -*- coding: utf-8 -*-
"""검증기를 넓힌 뒤 남은 실험실 코드 3편."""
from _common import make, write

E = {}
ep = make(E)

ep('CS0197', 'Player.cs',
   "Passing 'Player.hp' as ref or out may cause a runtime exception", """
using System;
using UnityEngine;

public class Player : MarshalByRefObject
{
    public int hp = 100;

    void Bump(ref int value)
    {
        value++;
    }

    void Start()
    {
        Bump(ref hp);
    }
}
""", """
using System;
using UnityEngine;

public class Player
{
    public int hp = 100;

    void Bump(ref int value)
    {
        value++;
    }

    void Start()
    {
        Bump(ref hp);
    }
}
""", 4)

ep('CS0217', 'Gold.cs',
   "To be usable as a short circuit operator, operator & must return type 'Gold'", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static int operator &(
        Gold left, Gold right) => default;

    public static bool operator true(
        Gold coin) => true;

    public static bool operator false(
        Gold coin) => false;
}

public class Wallet : MonoBehaviour
{
    public Gold coins;
    bool Both() => coins && coins;
}
""", """
using UnityEngine;

public struct Gold
{
    public int amount;

    public static Gold operator &(
        Gold left, Gold right) => default;

    public static bool operator true(
        Gold coin) => true;

    public static bool operator false(
        Gold coin) => false;
}

public class Wallet : MonoBehaviour
{
    public Gold coins;
    bool Both() => coins && coins;
}
""", 7)

ep('CS1064', 'Game.cs',
   "The best Add method 'Bag.Add(int)' for the collection initializer is obsolete", """
using System;
using System.Collections;
using UnityEngine;
public class Bag : IEnumerable
{
    [Obsolete]
    public void Add(int id) { }
    public void Add(string name) { }
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
    }
}
""", """
using System;
using System.Collections;
using UnityEngine;
public class Bag : IEnumerable
{

    public void Add(int id) { }
    public void Add(string name) { }
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
    }
}
""", 6)

if __name__ == '__main__':
    write(E, 'final.json')
