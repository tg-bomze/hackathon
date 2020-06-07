using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor.UI;
using UnityEngine.UI;

public class menu : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    public void create_project() {
        GameObject o = GameObject.Find("ui_CreateProject");
        o.GetComponent<Animation>().Play("menu_to_bottom", AnimationPlayMode.Queue);
    }
    public void create_project_off() {
        GameObject o = GameObject.Find("ui_CreateProject");
        o.GetComponent<Animation>().Play("menu_of_bottom", AnimationPlayMode.Queue);
    }
    public void create_startup() {
        string[] j = new  string [7];
        j[0] = GameObject.Find("name").GetComponent<InputField>().text;
        j[1] = GameObject.Find("krops").GetComponent<InputField>().text;
        j[2] = GameObject.Find("idea").GetComponent<InputField>().text;
        j[3] = GameObject.Find("Goal").GetComponent<InputField>().text;
        j[4] = GameObject.Find("Coast").GetComponent<InputField>().text;
        j[5] = GameObject.Find("krops").GetComponent<InputField>().text;
        ini.send("{\"type\": \"createStartup\", \"value\": {\"name\":\""+j[0]+"\"}}");
    }
}
