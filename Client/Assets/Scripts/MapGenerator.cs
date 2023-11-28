using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MapGenerator : MonoBehaviour
{

    [Header("Objects")]
    public GameObject rappi;
    public GameObject googleMaps;
    public GameObject food;
    public GameObject deposit;
    private APIHelper apiHelper;
    public Transform Objects;

    [Header("Variables")]
    public float x;
    public float y;
    public float z;

    void Start()
    {
        Objects = new GameObject("Objects").transform;
        apiHelper = new APIHelper();
        Steps stepsData = apiHelper.Start();
        List<Step> steps = stepsData.steps;

        DepositLocation depositLocation = stepsData.deposit_location;

        x = depositLocation.x;
        z = depositLocation.y;
        
        Vector3 spawnPosition = new Vector3(x, y, z);
        Quaternion spawnRotation = Quaternion.Euler(-90f, 0f, 0f);
        GameObject newDeposit = Instantiate(deposit, spawnPosition, spawnRotation, Objects);

        Step firstStep = steps[0];
        foreach (Agent agent in firstStep.agents)
        {
            if (agent.type == "Rappi")
            {
                x = agent.x;
                z = agent.y;
                spawnPosition = new Vector3(x * 10, 0, z * 10);
                spawnRotation = Quaternion.Euler(0f, 0f, 0f);
                GameObject newRappi = Instantiate(this.rappi, spawnPosition, spawnRotation, Objects);
                newRappi.tag = agent.id;
                
            }
            else if (agent.type == "GoogleMaps")
            {
                x = agent.x;
                z = agent.y;
                spawnPosition = new Vector3(x * 10, 0, z * 10);
                spawnRotation = Quaternion.Euler(0f, 0f, 0f);
                GameObject newGoogleMaps = Instantiate(this.googleMaps, spawnPosition, spawnRotation, Objects);
                newGoogleMaps.tag = agent.id;
            }
            else
            {
                Debug.Log("Error: Agent type not found");
            }
        }

        foreach (Food food in firstStep.food)
        {
            x = food.x;
            z = food.y;
            spawnPosition = new Vector3(x * 10, 0, z * 10);
            spawnRotation = Quaternion.Euler(0f, 0f, 0f);
            GameObject newFood = Instantiate(this.food, spawnPosition, spawnRotation, Objects);
        }

        StartCoroutine(UpdateAgents(steps));

    }

    IEnumerator UpdateAgents(List<Step> steps)
    {
        foreach (Step step in steps)
        {
            yield return new WaitForSeconds(1f);
            GameObject[] gos;
            foreach (Agent agent in step.agents)
            {
                x = agent.x;
                z = agent.y;
                gos = GameObject.FindGameObjectsWithTag(agent.id);
                if (gos != null)
                {
                    gos[0].transform.position = new Vector3(x * 10, 0, z * 10);
                }
                else
                {
                    Debug.Log("Error: Agent type not found");
                }
            }
        }
    }
}
