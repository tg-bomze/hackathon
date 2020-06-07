using System.Collections;
using System.Collections.Generic;
using System.Collections.Specialized;
using UnityEngine;
using UnityEngine.Experimental.Rendering;
using UnityEngine.UI;
public class camera : MonoBehaviour
{
    Camera cam = null;
    GameObject room = null;
    GameObject pr = null;
    public GameObject hi_pref;
    public GameObject prefab_pr;

    public GameObject ui_act;
    public GameObject ui_inact;
    // Start is called before the first frame update
    void Start()
    {
        cam = this.GetComponent<Camera>();
        room = GameObject.FindGameObjectWithTag("room");
        ini.cam = this;
        ini.start();
        ini.send("{\"type\": \"auth\"}");

    }

    public void render_me(auth a) {
        if (a.result) {
            pr = Instantiate(prefab_pr, new Vector3(), new Quaternion());
            usr p = pr.GetComponent<usr>();
            p.ini(a.value.photo);
            p.id = a.value.id;
            p.name = a.value.name;
            p.position = new Vector3((float) a.value.coord[0], (float) a.value.coord[0], 0);
            p.status = a.value.status;
        }
    }

    public void render_or(user_info a)
    {
        if (ini.finBbyId(a.id) == null)
        {
            GameObject ty = Instantiate(prefab_pr, new Vector3(), new Quaternion());
            ty.name = "fd_" + a.id;
            usr p = ty.GetComponent<usr>();
            p.ini(a.photo);
            p.id = a.id;
            p.position = new Vector3((float)a.coord[0], (float)a.coord[0], 0);
            p.status = a.status;
            ty.transform.position = new Vector3((float)a.coord[0], (float)a.coord[0], 0);
        }
        else {
            GameObject ty = ini.finBbyId(a.id);
            ty.transform.position = new Vector3((float)a.coord[0], (float)a.coord[0], 0);
        }
        
    }

    // Update is called once per frame
    float old_dist = 0f;
    float cam_size = 8f;
    Vector3 down_map = new Vector3();
    Vector3 cur_map = new Vector3();
    bool upblock = false;
    void Update()
    {
        if (Input.mousePosition.y < Screen.height * 0.8f && Input.mousePosition.y > Screen.height * 0.3f)
        {
            if (Input.GetMouseButtonDown(0))
            {
                down_map = Input.mousePosition;
                cur_map = down_map;
                Vector2 mousePosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
                GameObject[] n = GameObject.FindGameObjectsWithTag("button");
                Collider2D c = new Collider2D();

                Ray ray = cam.ScreenPointToRay(Input.mousePosition);
                RaycastHit hit;
                if (Physics.Raycast(ray, out hit, 1000f))
                {
                    if (hit.transform.tag == "button") { upblock = true; }
                    if (hit.transform.name == "hi_ico2")
                    {
                        if (hit.transform.gameObject.GetComponent<stats>().id != (string)ini.getStat("id"))
                        {
                            hi_otv(hit.transform.gameObject.GetComponent<stats>().id);
                        }
                       
                    }
                   
                }
                
                
            }
            if (Input.GetMouseButton(0))
            {
                if ((cur_map - Input.mousePosition).magnitude > 7)
                {
                    //transform.position += ((cur_map - Input.mousePosition)/50);

                    Vector3 correct = ((cur_map - Input.mousePosition) / 50);
                    Vector3 pos = transform.position + correct;
                    Vector3 delta_pos = pos - room.transform.position;
                    if (delta_pos.x > 10 || delta_pos.x < -10) { correct.x = 0; }
                    if (delta_pos.y > 10 || delta_pos.y < -10) { correct.y = 0; }
                    transform.position += correct;
                    cur_map = Input.mousePosition;
                }

            }
            if (Input.GetMouseButtonUp(0))
            {
                if (!upblock)
                {
                    if ((down_map - Input.mousePosition).magnitude <= 1)
                    {
                        Vector2 vos = new Vector2();
                        Vector3 point = new Vector3(Input.mousePosition.x - (Screen.width / 2), Input.mousePosition.y - (Screen.height / 2), 4.25f);
                        point.x = point.x / (Screen.width / 2);
                        point.y = point.y / (Screen.height / 2);
                        Vector3 ve = Camera.main.WorldToScreenPoint(GameObject.FindGameObjectWithTag("u2w").GetComponent<Renderer>().bounds.center);
                        ve.x = ve.x - Screen.width / 2;
                        point.x = cam.transform.position.x + ((Input.mousePosition.x - Screen.width / 2) / ve.x);
                        point.y = cam.transform.position.y + ((Input.mousePosition.y - Screen.height / 2) / ve.x);

                        point.z = -4.7f;
                        pr.transform.position = point;

                        ini.send("{\"type\": \"setPosition\", \"value\": [" + vos.x + "," + vos.y + "]}");
                    }


                    if (Input.touchCount == 2)
                    {
                        Touch touch_1 = Input.GetTouch(0);
                        Touch touch_2 = Input.GetTouch(1);
                        float dist = (touch_1.position - touch_2.position).magnitude;
                        if (dist < old_dist)
                        {
                            cam_size += 0.3f;
                            if (cam_size > 30) { cam_size = 30f; }
                            cam.orthographicSize = cam_size;
                        }
                        else if (dist > old_dist)
                        {
                            cam_size -= 0.3f;
                            if (cam_size < 8) { cam_size = 8f; }
                            cam.orthographicSize = cam_size;
                        }
                        old_dist = dist;
                    }
                }
                upblock = false;
            }
        }
    }
    bool togle_translition = true;
    public void toogle_c()
    {
        if (togle_translition)
        {
            GameObject.Find("AutoTranslate").transform.GetChild(0).gameObject.SetActive(false);
            GameObject.Find("AutoTranslate").transform.GetChild(1).gameObject.SetActive(true);
        }
        else {
            GameObject.Find("AutoTranslate").transform.GetChild(1).gameObject.SetActive(false);
            GameObject.Find("AutoTranslate").transform.GetChild(0).gameObject.SetActive(true);
        }
        togle_translition = !togle_translition;
    }
    public void hellou() {
        ini.send("{\"type\": \"sendMessage\", \"id\": \""+ini.getStat("id")+"\", \"value\": {\"status\":2, \"text\":\"hi\"}}");
        ui_act.SetActive(false);
        ui_inact.SetActive(true);
        Vector3 v3 = new Vector3(-10.1f, 1f, 0f);       
        GameObject go = Instantiate(hi_pref, pr.transform,true);
       // go.transform.SetParent(pr.transform);
        //Debug.Log("soso");
       // go.transform.localPosition = new Vector3(0.1f, 1f, 0f);
        
    }
    void hi_otv(string e) {
        Debug.Log("true_hi");
        ini.send("{\"type\": \"sendMessage\", \"id\": \""+e+"\", \"value\": {\"status\":3, \"text\":\"hi\"}}");
    }

    public void send(InputField e) {
        ini.send("{\"type\": \"sendMessage\", \"id\": \"" + ini.getStat("id") + "\", \"value\": {\"status\":1, \"text\":\""+e.text+"\"}}");

    }

    public void add_push(string e, string id)
    {

    }
}

