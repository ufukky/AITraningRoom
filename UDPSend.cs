using UnityEngine;
using System.Collections;
 
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
 
public class UDPSend
{
    // prefs
    public string IP = "127.0.0.1";
    public int port;
    IPEndPoint remoteEndPoint;
    UdpClient client;

    public UDPSend(int port = 8080,string IP = "127.0.0.1")
        {this.IP = IP;this.port = port;}
      
    // init
    public void init()
    {
        remoteEndPoint = new IPEndPoint(IPAddress.Parse(IP), port);
        client = new UdpClient();
        client.Connect(remoteEndPoint);
    }
  
    // sendData
    public void sendString(string message)
    {
        try
        {
            byte[] data = Encoding.UTF8.GetBytes(message);
            client.Send(data, data.Length);
        }
        catch (Exception err)
        {
            Debug.Log(err);
        }
    }
}