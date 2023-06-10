using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Camera))]
public class TargetCameraController : MonoBehaviour
{
    [SerializeField] Transform target;
    public float posX,posY;
    Camera cam;
    // Start is called before the first frame update
    void Start()
    {
        cam = GetComponent<Camera>();
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 targetScreenPos = cam.WorldToScreenPoint(target.position);
        posX = (targetScreenPos.x/Screen.width - 0.5f) * 2f;
        posY = (targetScreenPos.y/Screen.height - 0.5f) * 2f;
    }
}
