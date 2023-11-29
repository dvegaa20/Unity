using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

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
    public Vector3 food_pos;
    Vector3 spawnPosition;
    Quaternion spawnRotation = Quaternion.Euler(-90f, 0f, 0f);

    void Start()
    {
        Objects = new GameObject("Objects").transform;
        apiHelper = new APIHelper();
        Steps stepsData = apiHelper.Start();
        List<Step> steps = stepsData.steps;
        List<PickingSteps> pickingSteps = stepsData.picking_steps;
        DepositLocation depositLocation = stepsData.deposit_location;

        x = depositLocation.x;
        z = depositLocation.y;

        spawnPosition = new Vector3(x * 10, y, z * 10);
        
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

        StartCoroutine(UpdateAgents(steps, pickingSteps));
        StartCoroutine(SpawnFood(steps));

    }

    IEnumerator UpdateAgents(List<Step> steps, List<PickingSteps> pickingSteps)
    {
        StepCountManager stepCountManager = FindObjectOfType<StepCountManager>();
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
            int currentStep = stepCountManager.GetCurrentStepCount();
            Debug.Log("Step: " + currentStep);
            stepCountManager.IncrementStepCount();
        }
    }

    IEnumerator SpawnFood(List<Step> steps){
        foreach(Step step in steps){
            if (step.id % 5 == 0)
            {
                yield return new WaitForSeconds(5f);
                foreach (Food food in step.food)
                {
                    x = food.x;
                    z = food.y;
                    spawnPosition = new Vector3(x * 10, 0, z * 10);
                    spawnRotation = Quaternion.Euler(0f, 0f, 0f);
                    GameObject newFood = Instantiate(this.food, spawnPosition, spawnRotation, Objects);
                }
            }
        }
    }
}
