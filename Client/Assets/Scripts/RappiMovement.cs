using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RappiMovement : MonoBehaviour
{
    public float speed = 5f;
    public float rotation = 180f;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
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
            Debug.Log("colision con: " + collision.gameObject.tag);
            // Si choca con un objeto etiquetado como "Obstacle", dar media vuelta
            TurnAround();
        }
    }

    private void TurnAround()
    {
        transform.Rotate(Vector3.up, rotation); // Media vuelta en el eje Y
    }
}
