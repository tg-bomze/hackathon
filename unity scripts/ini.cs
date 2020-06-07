using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System;
using System.Text;

public static class ini
{
    static string ip_server = "127.0.0.1";
    static int port = 65433;
    static Socket sk = null;
    public static camera cam;
    // Start is called before the first frame update
    public static void start()
    {
        IPEndPoint ipPoint = new IPEndPoint(IPAddress.Parse(ip_server), port);
        sk = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
      //  sk.Connect(ipPoint);
    }
    static string old_m = "";
    public static void send(string e) {      

        if (sk != null)
        {
            byte[] bufer = Encoding.UTF8.GetBytes(e);
            byte[] b = BitConverter.GetBytes(bufer.Length);
            sk.Send(b);            
            sk.Send(bufer);
            old_m = e;
        }
       
    }

    static void do_send(string e) {
        if (sk != null)
        {
            byte[] bufer = Encoding.UTF8.GetBytes(e);
            sk.Send(bufer);
        }
    }
    static void reciver()
    {
        if (sk != null)
        {
            byte[] data = new byte[256];
            StringBuilder builder = new StringBuilder();
            int bytes = 0;

            do
            {
                data = new byte[sk.Available];
                bytes = sk.Receive(data, data.Length, 0);
                builder.Append(Encoding.UTF8.GetString(data, 0, bytes));
            }
            while (sk.Available > 0);
            new recive().ini(builder.ToString());
            String b = builder.ToString();
            if (old_m.IndexOf("auth") != -1)
            {
                auth a = JsonUtility.FromJson<auth>(b);
                cam.render_me(a);
            }

            if (old_m.IndexOf("setPosition") != -1) {
                user_info [] a = JsonUtility.FromJson<user_info []>(b);
                for (int w = 0; w < a.Length; w++) {
                    cam.render_or(a[w]);
                }
            }

            if (b.IndexOf("sendMessage") != -1)
            {
                mess a = JsonUtility.FromJson<mess>(b);
                if (a.value.status == 1) {
                    GameObject g = finBbyId(a.id);
                    if (g != null) {
                        g.GetComponent<usr>().sendMess(a.value.text);
                    }
                }
                if (a.value.status == 2 || a.value.status == 3)
                {
                    GameObject g = finBbyId(a.id);
                    if (g != null)
                    {
                        g.GetComponent<usr>().sendhi();
                    }
                }
            }
           

        }
        else
        {
            reciver();
        }
    }
    static Dictionary<String, UnityEngine.Object> pref = new Dictionary<String, UnityEngine.Object>();
    public static System.Object getStat(string e) {
        if (pref.ContainsKey(e))
        {
            return pref[e];
        }
        else {
            return null;
        }
    }

    public static GameObject finBbyId(string e) {
        GameObject g = GameObject.Find("fd_" + e);
        return g;
    }

}

public class user_info {
    public string id;
    public int status;
    public System.Object[] coord;
    public string text_orig;
    public string text_trans;
    public string photo;
}

public class auth {
    public bool result;
    public auth_st value;

}
public class auth_st {
    public string id;
    public int status;
    public System.Object[] coord;
    public string photo;
    public string name;
}

public class mess {
    public string type;
    public string id;
    public mess_m value;
}
public class mess_m {
    public string text;
    public int status;
}
public class uio {
    user_info[] o;
}