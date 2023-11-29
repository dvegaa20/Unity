using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.IO;

public class APIHelper : MonoBehaviour
{
    public Steps Start()
    {
        Debug.Log("Fetching API data...");
        HttpWebRequest request = (HttpWebRequest)WebRequest.Create("http://localhost:8585");
        HttpWebResponse response = (HttpWebResponse)request.GetResponse();
        
        using (StreamReader reader = new StreamReader(response.GetResponseStream()))
        {
            string json = reader.ReadToEnd();
            return JsonUtility.FromJson<Steps>(json);
        }
    }
}
