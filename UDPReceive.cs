
using UnityEngine;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Collections.Generic;
using System.Linq;
using System.Collections.Concurrent;
using Unity.Profiling;

public class UDPReceive
{
    UdpClient client;
    public int port; // define > init
    public List<string> packages;
    string _lastGettedPackage;
    public string ip = "127.0.0.1";

    static readonly ProfilerMarker GetNewPackageMarker = new ProfilerMarker("UDPReceive.GetNewPackage");
    ConcurrentQueue<byte[]> ReceivedPacketQueue = new ConcurrentQueue<byte[]>();
    IPEndPoint _ipEndPoint;
    public UDPReceive(int port)
        {this.port = port;packages = new List<string>();}
       
    // init
    public void init()
    {
        _ipEndPoint = new IPEndPoint(IPAddress.Parse(ip), port);
        client = new UdpClient();
        client.Client.Bind(_ipEndPoint);
        client.BeginReceive(OnUdpData, client);
        /*
        receiveThread = new Thread(
            new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
        */
    }
    private void OnUdpData(IAsyncResult result) 
    {
        var socket = result.AsyncState as UdpClient;
        var message = socket.EndReceive(result, ref _ipEndPoint);
        try
        {
            checkData(message, out string _str);
        }            
        catch (Exception err)
        {
            Debug.Log(err);
        }
        
        ReceivedPacketQueue.Enqueue(message);
        socket.BeginReceive(OnUdpData, socket);
    }

    private bool checkData(byte[] data,out string data_str)
    {
        data_str = "";
        try
        {
            string text = Encoding.UTF8.GetString(data);
            if (text.Length > 0)
            {
                packages.Add(text);
                if (packages.Count > 100)
                    packages.Take(100);
            }
            data_str = text;
            return true;
        }
        catch (Exception err)
        {
            Debug.Log(err);
            return false;
        }
    }
    private void ReceiveData()
    {
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                if(checkData(client.Receive(ref anyIP),out string str)) 
                {
                    
                }
            }
            catch (Exception err)
            {
                Debug.Log(err);
            }
        }
    }


    public bool GetNewPackage(out string outPackage)
    {
        using (GetNewPackageMarker.Auto()) 
        { 
            outPackage = null;
            if(_lastGettedPackage == null)
            {
                if(packages.Count > 0)
                {
                    _lastGettedPackage = packages[packages.Count-1];
                    outPackage = _lastGettedPackage;
                    return true;
                }
                return false;  
            }

            if(_lastGettedPackage == packages[packages.Count-1])
                return false;
        
            _lastGettedPackage = packages[packages.Count-1];
            outPackage = _lastGettedPackage;
            return true;
        }   
    }
}