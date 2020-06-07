using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class usr : MonoBehaviour
{
    public string id = "";
    public Vector3 position = new Vector3();
    public string name = "";
    public string f_name = "";
    public Texture2D img = null;
    public int status = 0;
    public GameObject hi_pref;
    // Start is called before the first frame update
    void Start()
    {
       
    }
    public void ini(string i) {
        byte[] b = System.Convert.FromBase64String(i);
        img = new Texture2D(1, 1);
        img.LoadImage(b);
    }
    // Update is called once per frame
    void Update()
    {
        
    }

    public void sendMess(string e) {
        GameObject g = GameObject.Find("chat");
        GameObject c = GameObject.Find("Canvas");
        g = Instantiate(g, new Vector3(), new Quaternion(),c.transform);
        g.SetActive(true);
        g.transform.GetChild(0).GetComponent<Text>().text = e;
        g.transform.GetChild(0).GetComponent<depth_time>().str();
    }
    public void sendhi()
    {
        Vector3 v3 = new Vector3(-10.1f, 1f, 0f);
        GameObject go = Instantiate(hi_pref, transform, true);
    }
}
