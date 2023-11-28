using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GoogleMovement : MonoBehaviour
{
    public float speed = 5f;
    public float rotation = 180f;

    void Update()
    {
        moveForward();
    }

    void moveForward()
    {
        transform.Translate(Vector3.forward * speed * Time.deltaTime);
    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("Wall") || collision.gameObject.CompareTag("Rappi") || collision.gameObject.CompareTag("Google"))
        {
            TurnAround();
        }
    }

    private void TurnAround()
    {
        transform.Rotate(Vector3.up, rotation);
    }
}
