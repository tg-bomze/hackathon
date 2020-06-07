using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class depth_time : MonoBehaviour
{
    public float time = 10f;
    public bool st = true;
    public bool pos = true;
    // Start is called before the first frame update
    void Start()
    {
        transform.position = new Vector3(0.1f, 1f, 0f);
    }

    // Update is called once per frame

    public void str() {
        st = true;
    }
    void Update()
    {
        if (st) {
            time -= +Time.deltaTime;
            if (pos) { transform.localPosition = new Vector3(0.1f, 1f, 0f); }
            if (time <= 0) {
                Destroy(gameObject);
            }
        }
    }
}
