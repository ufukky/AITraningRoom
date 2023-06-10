using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetController : MonoBehaviour
{
    public float setDistance = 25f;
    public float changeDirTime = 4f;
    public float divRadius = 10f;
    public float speed = 5f;
    public Transform fixedWing;
    // Start is called before the first frame update

    float _changeDirT = 0f;
    void Start()
    {
        _changeDirT = changeDirTime;
    }

    // Update is called once per frame
    void Update()
    {
        transform.position += Vector3.forward * speed * Time.deltaTime;
        
        if(_changeDirT <= 0f)
        {
            transform.position = new Vector3(Random.Range(-1 * divRadius, divRadius), Random.Range(-1 * divRadius, divRadius), transform.position.z);
            _changeDirT = changeDirTime;
        }

        _changeDirT -= Time.deltaTime;
    }
}
