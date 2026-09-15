# -*- coding: utf-8 -*-
"""2티어 앞부분 리라이트: 리터럴·전처리기·제어 흐름 구문 에러."""
from _common import make, write

E = {}
ep = make(E)

# 37 CS1001 — 필드 이름을 바꾸다가 이름만 지웠다.
ep('CS1001', 'Player.cs', "Identifier expected", """
using UnityEngine;

public class Player : MonoBehaviour
{
    public int hp = 100;
    public int mana = 50;
    public int = 20;
    public int defense = 10;

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
    public int stamina = 20;
    public int defense = 10;

    void Start()
    {
        Debug.Log(hp);
    }
}
""", 7)

# 38 CS1004 — static 을 붙이면서 이미 있던 걸 못 봤다.
ep('CS1004', 'SaveTools.cs', "Duplicate 'static' modifier", """
using UnityEngine;

public class SaveTools : MonoBehaviour
{
    public static int slot = 1;

    public static static void Save()
    {
        Debug.Log("Saved slot " + slot);
    }

    public static void Load()
    {
        Debug.Log("Loaded");
    }
}
""", """
using UnityEngine;

public class SaveTools : MonoBehaviour
{
    public static int slot = 1;

    public static void Save()
    {
        Debug.Log("Saved slot " + slot);
    }

    public static void Load()
    {
        Debug.Log("Loaded");
    }
}
""", 7)

# 39 CS1009 — 탐색기에서 복사한 윈도우 경로를 그대로 붙였다.
ep('CS1009', 'SaveFile.cs', "Unrecognized escape sequence", """
using UnityEngine;
using System.IO;

public class SaveFile : MonoBehaviour
{
    string folder = "C:\\Games\\Save";

    void Start()
    {
        Debug.Log(folder);
    }

    public bool Exists()
    {
        return Directory.Exists(folder);
    }
}
""", """
using UnityEngine;
using System.IO;

public class SaveFile : MonoBehaviour
{
    string folder = @"C:\\Games\\Save";

    void Start()
    {
        Debug.Log(folder);
    }

    public bool Exists()
    {
        return Directory.Exists(folder);
    }
}
""", 6)

# 40 CS1010 — 대사를 치다가 닫는 따옴표 전에 엔터를 쳤다.
ep('CS1010', 'Dialogue.cs', "Newline in constant", """
using UnityEngine;
using UnityEngine.UI;

public class Dialogue : MonoBehaviour
{
    public Text box;

    void Start()
    {
        string line = "Welcome to Bug
        box.text = line;
    }

    public void Clear()
    {
        box.text = "";
    }
}
""", """
using UnityEngine;
using UnityEngine.UI;

public class Dialogue : MonoBehaviour
{
    public Text box;

    void Start()
    {
        string line = "Welcome to Bug";
        box.text = line;
    }

    public void Clear()
    {
        box.text = "";
    }
}
""", 10)

# 41 CS1011 — 스페이스바를 넣는다는 게 따옴표만 남겼다.
ep('CS1011', 'InputKeys.cs', "Empty character literal", """
using UnityEngine;

public class InputKeys : MonoBehaviour
{
    public char jumpKey = '';
    public char fireKey = 'F';

    void Update()
    {
        Debug.Log(jumpKey);
    }
}
""", """
using UnityEngine;

public class InputKeys : MonoBehaviour
{
    public char jumpKey = ' ';
    public char fireKey = 'F';

    void Update()
    {
        Debug.Log(jumpKey);
    }
}
""", 5)

# 42 CS1012 — 버튼 이름이 두 글자인데 char 로 받았다.
ep('CS1012', 'PadKeys.cs', "Too many characters in character literal", """
using UnityEngine;

public class PadKeys : MonoBehaviour
{
    public char jumpKey = 'A';
    public char fireKey = 'LB';

    void Update()
    {
        Debug.Log(fireKey);
    }
}
""", """
using UnityEngine;

public class PadKeys : MonoBehaviour
{
    public char jumpKey = 'A';
    public string fireKey = "LB";

    void Update()
    {
        Debug.Log(fireKey);
    }
}
""", 6)

# 43 CS1013 — 16진수 색상값을 적다 말았다.
ep('CS1013', 'Palette.cs', "Invalid number", """
using UnityEngine;

public class Palette : MonoBehaviour
{
    public int enemyTint = 0x;
    public int allyTint = 0x33FF88;

    void Start()
    {
        Debug.Log(enemyTint);
    }
}
""", """
using UnityEngine;

public class Palette : MonoBehaviour
{
    public int enemyTint = 0xFF5544;
    public int allyTint = 0x33FF88;

    void Start()
    {
        Debug.Log(enemyTint);
    }
}
""", 5)

# 44 CS1021 — 자릿수를 세지 않고 9를 눌러 채웠다.
ep('CS1021', 'Wallet.cs', "Integral constant is too large", """
using UnityEngine;

public class Wallet : MonoBehaviour
{
    ulong gold = 99999999999999999999;
    public int gems = 500;

    void Start()
    {
        Debug.Log("Gold: " + gold);
    }

    public void Spend(int cost)
    {
        gems -= cost;
    }
}
""", """
using UnityEngine;

public class Wallet : MonoBehaviour
{
    ulong gold = 9999999999999999999;
    public int gems = 500;

    void Start()
    {
        Debug.Log("Gold: " + gold);
    }

    public void Spend(int cost)
    {
        gems -= cost;
    }
}
""", 5)

# 45 CS1039 — 축자 문자열을 닫지 않았다.
ep('CS1039', 'LevelPaths.cs', "Unterminated string literal", """
using UnityEngine;

public class LevelPaths : MonoBehaviour
{
    string root = @"Assets/Levels;
    public int levelCount = 12;

    void Start()
    {
        Debug.Log(root);
    }
}
""", """
using UnityEngine;

public class LevelPaths : MonoBehaviour
{
    string root = @"Assets/Levels";
    public int levelCount = 12;

    void Start()
    {
        Debug.Log(root);
    }
}
""", 5)

# 46 CS1056 — 파이썬 습관으로 주석을 # 으로 달았다.
ep('CS1056', 'Health.cs', "Unexpected character '#'", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        # starting health
        Debug.Log(hp);
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        // starting health
        Debug.Log(hp);
    }
}
""", 9)

# 47 CS1073 — 재대입하면서 타입을 지우다 말았다.
ep('CS1073', 'Health.cs', "Unexpected token 'int'", """
using UnityEngine;

public class Health : MonoBehaviour
{
    void Start()
    {
        int hp = 100;
        int mana = 50;

        hp = int 80;
        mana = 20;
        Debug.Log(hp + mana);
    }
}
""", """
using UnityEngine;

public class Health : MonoBehaviour
{
    void Start()
    {
        int hp = 100;
        int mana = 50;

        hp = 80;
        mana = 20;
        Debug.Log(hp + mana);
    }
}
""", 10)

# 48 CS1041 — 변수 이름을 키워드로 지었다.
ep('CS1041', 'Enemy.cs', "Identifier expected; 'class' is a keyword", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int tier = 1;

    void Spawn()
    {
        string class = "elite" + tier;
        Debug.Log("Tier " + tier);
    }
}
""", """
using UnityEngine;

public class Enemy : MonoBehaviour
{
    public int tier = 1;

    void Spawn()
    {
        string rank = "elite" + tier;
        Debug.Log("Tier " + tier);
    }
}
""", 9)

# 49 CS1043 — 식 본문 속성을 쓰다 말았다.
ep('CS1043', 'Player.cs', "{ or ; expected", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp = 100;
    int armor = 10;

    public int Hp => hp;
    public int Armor => armor;
    public int Defense =>

    void Start()
    {
        Debug.Log(Hp);
    }
}
""", """
using UnityEngine;

public class Player : MonoBehaviour
{
    int hp = 100;
    int armor = 10;

    public int Hp => hp;
    public int Armor => armor;
    public int Defense => armor * 2;

    void Start()
    {
        Debug.Log(Hp);
    }
}
""", 10)

# 50 CS1044 — 반복 변수를 하나 더 두면서 타입까지 같이 적었다.
ep('CS1044', 'Waves.cs',
   "Cannot use more than one type in a for, using, fixed, or declaration statement", """
using UnityEngine;

public class Waves : MonoBehaviour
{
    void Start()
    {
        for (int i = 0, long n; i < 3;)
        {
            Debug.Log("Wave " + i++);
        }
    }
}
""", """
using UnityEngine;

public class Waves : MonoBehaviour
{
    void Start()
    {
        for (int i = 0, n = 0; i < 3;)
        {
            Debug.Log("Wave " + i++);
        }
    }
}
""", 7)

# 51 CS1023 — 중괄호 없는 if 안에서 변수를 선언했다.
ep('CS1023', 'Loot.cs',
   "Embedded statement cannot be a declaration or labeled statement", """
using UnityEngine;

public class Loot : MonoBehaviour
{
    public bool isBoss = true;

    void Start()
    {
        if (isBoss)
            int drops = 5;
        Debug.Log("Rolling loot");
    }
}
""", """
using UnityEngine;

public class Loot : MonoBehaviour
{
    public bool isBoss = true;

    void Start()
    {
        if (isBoss)
            { int drops = 5; }
        Debug.Log("Rolling loot");
    }
}
""", 10)

# 52 CS1035 — 코드를 잠깐 막아두려고 연 블록 주석을 안 닫았다.
ep('CS1035', 'Notes.cs', 'End-of-file found, "*/" expected', """
using UnityEngine;

public class Notes : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        /* warm up */
        Debug.Log(hp);

        /* disabled for now
        Heal();
    }

    void Heal()
    {
        hp = 100;
    }
}
""", """
using UnityEngine;

public class Notes : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
        /* warm up */
        Debug.Log(hp);

        /* disabled for now */
        Heal();
    }

    void Heal()
    {
        hp = 100;
    }
}
""", 12)

# 53 CS1024 — C 습관대로 #ifdef 를 썼다.
ep('CS1024', 'BuildFlags.cs', "Preprocessor directive expected", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    void Start()
    {
#ifdef UNITY_EDITOR
        Debug.Log("Editor build");
#endif
        Debug.Log("Game start");
    }
}
""", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    void Start()
    {
#if UNITY_EDITOR
        Debug.Log("Editor build");
#endif
        Debug.Log("Game start");
    }
}
""", 7)

# 54 CS1027 — #if 를 열어두고 닫는 걸 잊었다.
ep('CS1027', 'BuildFlags.cs', "#endif directive expected", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
#if UNITY_EDITOR
        Debug.Log("Editor only");

        Debug.Log("Always runs");
    }
}
""", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    public int hp = 100;

    void Start()
    {
#if UNITY_EDITOR
        Debug.Log("Editor only");
#endif
        Debug.Log("Always runs");
    }
}
""", 11)

# 55 CS1028 — #endif 자리에 손이 #endregion 을 쳤다.
ep('CS1028', 'BuildFlags.cs', "Unexpected preprocessor directive", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    void Start()
    {
#if UNITY_EDITOR
        Debug.Log("Editor only");
#endregion
#endif
        Debug.Log("Game start");
    }
}
""", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    void Start()
    {
#if UNITY_EDITOR
        Debug.Log("Editor only");

#endif
        Debug.Log("Game start");
    }
}
""", 9)

# 56 CS1029 — 빌드를 막아두려고 넣은 #error 가 그대로 남았다.
ep('CS1029', 'BuildGate.cs', "#error: build stopped here", """
using UnityEngine;

public class BuildGate : MonoBehaviour
{
    void Start()
    {
#if !UNITY_EDITOR
#error build stopped here
#endif
        Debug.Log("Game start");
    }
}
""", """
using UnityEngine;

public class BuildGate : MonoBehaviour
{
    void Start()
    {
#if !UNITY_EDITOR

#endif
        Debug.Log("Game start");
    }
}
""", 8)

# 57 CS1030 — 남겨둔 #warning 이 빌드 로그를 채운다.
ep('CS1030', 'Spawner.cs', "#warning: 'TODO: fix the spawn rate'", """
using UnityEngine;

public class Spawner : MonoBehaviour
{
#warning TODO: fix the spawn rate
    public float rate = 0.5f;

    void Start()
    {
        Debug.Log(rate);
    }

    void Spawn() { }
}
""", """
using UnityEngine;

public class Spawner : MonoBehaviour
{

    public float rate = 0.5f;

    void Start()
    {
        Debug.Log(rate);
    }

    void Spawn() { }
}
""", 5)

# 58 CS1038 — #region 을 열고 닫지 않았다.
ep('CS1038', 'Regions.cs', "#endregion directive expected", """
using UnityEngine;

public class Regions : MonoBehaviour
{
    #region setup
    public int hp = 100;
    public int mana = 50;

    void Start()
    {
        Debug.Log(hp);
    }

}
""", """
using UnityEngine;

public class Regions : MonoBehaviour
{
    #region setup
    public int hp = 100;
    public int mana = 50;

    void Start()
    {
        Debug.Log(hp);
    }
    #endregion
}
""", 13)

# 59 CS1040 — 지시문을 복사하다 코드 줄 끝에 붙였다.
ep('CS1040', 'BuildFlags.cs',
   "Preprocessor directives must appear as the first non-whitespace character on a line", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    void Start()
    {
#if UNITY_EDITOR
        int hp = 100; #if UNITY_EDITOR
        Debug.Log(hp);
#endif
    }
}
""", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    void Start()
    {
#if UNITY_EDITOR
        int hp = 100;
        Debug.Log(hp);
#endif
    }
}
""", 8)

# 60 CS1517 — 조건을 쓰기 전에 연산자를 먼저 쳤다.
ep('CS1517', 'BuildFlags.cs', "Invalid preprocessor expression", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    void Start()
    {
#if && UNITY_EDITOR
        Debug.Log("Editor only");
#endif
        Debug.Log("Game start");
    }
}
""", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    void Start()
    {
#if UNITY_EDITOR && DEBUG
        Debug.Log("Editor only");
#endif
        Debug.Log("Game start");
    }
}
""", 7)

# 61 CS1025 — 지시문 뒤에 블록 주석을 달았다.
ep('CS1025', 'BuildFlags.cs', "Single-line comment or end-of-line expected", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    void Start()
    {
#if UNITY_EDITOR /* editor only */
        Debug.Log("Editor tools on");
#endif
        Debug.Log("Game start");
    }
}
""", """
using UnityEngine;

public class BuildFlags : MonoBehaviour
{
    void Start()
    {
#if UNITY_EDITOR // editor only
        Debug.Log("Editor tools on");
#endif
        Debug.Log("Game start");
    }
}
""", 7)

# 62 CS0139 — 반복문 안에 있던 코드를 메서드로 빼면서 break 를 데려왔다.
ep('CS0139', 'Patrol.cs',
   "No enclosing loop out of which to break or continue", """
using UnityEngine;

public class Patrol : MonoBehaviour
{
    public Transform[] points;

    void Step(int index)
    {
        if (index >= points.Length)
        {
            break;
        }
        Debug.Log("Moving");
    }
}
""", """
using UnityEngine;

public class Patrol : MonoBehaviour
{
    public Transform[] points;

    void Step(int index)
    {
        if (index >= points.Length)
        {
            return;
        }
        Debug.Log("Moving");
    }
}
""", 11)

# 63 CS0140 — 재시도 라벨을 복사하면서 이름을 안 바꿨다.
ep('CS0140', 'Loader.cs', "The label 'retry' is a duplicate", """
using UnityEngine;

public class Loader : MonoBehaviour
{
    public int tries = 0;

    void Start()
    {
retry:
        tries++;
        if (tries < 3)
            goto retry;
retry:
        Debug.Log("Gave up");
    }
}
""", """
using UnityEngine;

public class Loader : MonoBehaviour
{
    public int tries = 0;

    void Start()
    {
retry:
        tries++;
        if (tries < 3)
            goto retry;
done:
        Debug.Log("Gave up");
    }
}
""", 13)

# 64 CS0159 — 라벨 이름을 바꾸고 goto 는 그대로 뒀다.
ep('CS0159', 'Loader.cs',
   'No such label "done" within the scope of the goto statement', """
using UnityEngine;

public class Loader : MonoBehaviour
{
    public int tries = 0;

    void Start()
    {
        tries++;
        if (tries > 3)
            goto done;
        Debug.Log("Retrying");
finish:
        Debug.Log("Stopped");
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
        if (tries > 3)
            goto finish;
        Debug.Log("Retrying");
finish:
        Debug.Log("Stopped");
    }
}
""", 11)

# 65 CS0158 — 안쪽 블록에 바깥과 같은 이름의 라벨을 뒀다.
ep('CS0158', 'Loader.cs',
   'The label "top" shadows another label by the same name in a contained scope', """
using UnityEngine;

public class Loader : MonoBehaviour
{
    void Start()
    {
top:
        Debug.Log("outer pass");
        {
top:
            Debug.Log("inner pass");
        }
        goto top;
    }
}
""", """
using UnityEngine;

public class Loader : MonoBehaviour
{
    void Start()
    {
top:
        Debug.Log("outer pass");
        {
inner:
            Debug.Log("inner pass");
        }
        goto top;
    }
}
""", 10)

# 66 CS0163 — case 하나에서 break 를 빠뜨렸다.
ep('CS0163', 'Difficulty.cs',
   "Control cannot fall through from one case label to another", """
using UnityEngine;

public class Difficulty : MonoBehaviour
{
    public void Apply(int level)
    {
        switch (level)
        {
            case 1:
                Debug.Log("Easy");

            case 2:
                Debug.Log("Normal");
                break;
        }
    }
}
""", """
using UnityEngine;

public class Difficulty : MonoBehaviour
{
    public void Apply(int level)
    {
        switch (level)
        {
            case 1:
                Debug.Log("Easy");
                break;
            case 2:
                Debug.Log("Normal");
                break;
        }
    }
}
""", 11)

# 67 CS0152 — case 를 복사하고 숫자를 안 바꿨다.
ep('CS0152', 'Difficulty.cs',
   "The switch statement contains more than one case with the label 1", """
using UnityEngine;

public class Difficulty : MonoBehaviour
{
    public void Apply(int level)
    {
        switch (level)
        {
            case 1:
                Debug.Log("Easy");
                break;
            case 1:
                Debug.Log("Hard");
                break;
        }
    }
}
""", """
using UnityEngine;

public class Difficulty : MonoBehaviour
{
    public void Apply(int level)
    {
        switch (level)
        {
            case 1:
                Debug.Log("Easy");
                break;
            case 3:
                Debug.Log("Hard");
                break;
        }
    }
}
""", 12)

# 68 CS0151 — 난이도를 float 로 두고 switch 에 넣었다.
ep('CS0151', 'Difficulty.cs',
   "A switch expression of integral type is required", """
using UnityEngine;

public class Difficulty : MonoBehaviour
{
    public float level = 1f;

    void Start()
    {
        switch (level)
        {
            case 1:
                Debug.Log("Easy");
                break;
        }
    }
}
""", """
using UnityEngine;

public class Difficulty : MonoBehaviour
{
    public int level = 1;

    void Start()
    {
        switch (level)
        {
            case 1:
                Debug.Log("Easy");
                break;
        }
    }
}
""", 5)

# 69 CS0153 — switch 안에 있던 코드를 메서드로 빼면서 goto case 를 데려왔다.
ep('CS0153', 'Difficulty.cs',
   "A goto case is only valid inside a switch statement", """
using UnityEngine;

public class Difficulty : MonoBehaviour
{
    public void Apply(int level)
    {
        if (level < 1)
        {
            goto case 1;
        }
        Debug.Log("Applied " + level);
    }
}
""", """
using UnityEngine;

public class Difficulty : MonoBehaviour
{
    public void Apply(int level)
    {
        if (level < 1)
        {
            level = 1;
        }
        Debug.Log("Applied " + level);
    }
}
""", 9)

# 70 CS1524 — try 만 쓰고 catch 를 안 붙였다.
ep('CS1524', 'SaveGame.cs', "Expected catch or finally", """
using UnityEngine;

public class SaveGame : MonoBehaviour
{
    void Load()
    {
        try
        {
            Debug.Log("Loading");
        }

        Debug.Log("Done");
    }
}
""", """
using UnityEngine;

public class SaveGame : MonoBehaviour
{
    void Load()
    {
        try
        {
            Debug.Log("Loading");
        }
        catch { }
        Debug.Log("Done");
    }
}
""", 11)

# 71 CS0155 — 자바스크립트처럼 문자열을 던졌다.
ep('CS0155', 'SaveGame.cs',
   "The type caught or thrown must be derived from System.Exception", """
using System;
using UnityEngine;

public class SaveGame : MonoBehaviour
{
    public string path = "save.json";

    void Load()
    {
        if (path == "")
        {
            throw "path is empty";
        }
        Debug.Log("Loading " + path);
    }
}
""", """
using System;
using UnityEngine;

public class SaveGame : MonoBehaviour
{
    public string path = "save.json";

    void Load()
    {
        if (path == "")
        {
            throw new Exception("bad");
        }
        Debug.Log("Loading " + path);
    }
}
""", 12)

# 72 CS0156 — 정리하고 다시 던지려다 catch 대신 finally 에 썼다.
ep('CS0156', 'SaveGame.cs',
   "A throw statement with no arguments is not allowed outside of a catch clause", """
using System;
using UnityEngine;

public class SaveGame : MonoBehaviour
{
    void Load()
    {
        try
        {
            Debug.Log("Loading");
        }
        finally
        {
            throw;
        }
    }
}
""", """
using System;
using UnityEngine;

public class SaveGame : MonoBehaviour
{
    void Load()
    {
        try
        {
            Debug.Log("Loading");
        }
        catch
        {
            throw;
        }
    }
}
""", 12)

# 73 CS0157 — finally 에서 결과를 돌려주려 했다.
ep('CS0157', 'SaveGame.cs',
   "Control cannot leave the body of a finally clause", """
using UnityEngine;

public class SaveGame : MonoBehaviour
{
    public bool Load()
    {
        try
        {
            Debug.Log("Loading");
            return true;
        }
        finally
        {
            return false;
        }
    }
}
""", """
using UnityEngine;

public class SaveGame : MonoBehaviour
{
    public bool Load()
    {
        try
        {
            Debug.Log("Loading");
            return true;
        }
        finally
        {
            Debug.Log("Done");
        }
    }
}
""", 14)

# 74 CS0160 — 넓은 catch 를 먼저 써서 뒤가 죽었다.
ep('CS0160', 'SaveGame.cs',
   "A previous catch clause already catches all exceptions of this type", """
using System;
using UnityEngine;
public class SaveGame : MonoBehaviour
{
    void Load()
    {
        try
        {
            Debug.Log("Loading");
        }
        catch (Exception e)
        {
            Debug.Log(e.Message);
        }
        catch (FormatException e)
        {
            Debug.Log("Bad format");
        }
    }
}
""", """
using System;
using UnityEngine;
public class SaveGame : MonoBehaviour
{
    void Load()
    {
        try
        {
            Debug.Log("Loading");
        }
        catch (NullReferenceException e)
        {
            Debug.Log(e.Message);
        }
        catch (FormatException e)
        {
            Debug.Log("Bad format");
        }
    }
}
""", 11)

# 75 CS1017 — 전부 받는 catch 를 위에 두고 아래에 하나 더 붙였다.
ep('CS1017', 'SaveGame.cs',
   "Catch clauses cannot follow the general catch clause of a try statement", """
using System;
using UnityEngine;
public class SaveGame : MonoBehaviour
{
    void Load()
    {
        try
        {
            Debug.Log("Loading");
        }
        catch
        {
            Debug.Log("Failed");
        }
        catch (FormatException e)
        {
            Debug.Log("Bad format");
        }
    }
}
""", """
using System;
using UnityEngine;
public class SaveGame : MonoBehaviour
{
    void Load()
    {
        try
        {
            Debug.Log("Loading");
        }
        catch (ArgumentException)
        {
            Debug.Log("Failed");
        }
        catch (FormatException e)
        {
            Debug.Log("Bad format");
        }
    }
}
""", 11)

if __name__ == '__main__':
    write(E, 'tier2a.json')
