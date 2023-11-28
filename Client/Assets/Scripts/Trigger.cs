using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Trigger : MonoBehaviour
{
    private APIHelper apiHelper;
    private List<Step> steps;
    private List<PickingSteps> pickingSteps;

    void Start()
    {
        apiHelper = new APIHelper();
        Steps stepsData = apiHelper.Start();
        steps = stepsData.steps;
        pickingSteps = stepsData.picking_steps;
    }

    void OnTriggerEnter(Collider other)
    {
        if (steps != null && pickingSteps != null)
        {
            int step_count = 0;

            foreach (Step step in steps)
            {
                if (step_count == pickingSteps[0].step)
                {
                    if (other.gameObject.CompareTag("Food"))
                    {
                        Debug.Log("On Trigger Enter");
                        Destroy(other.gameObject);
                    }
                }
                step_count++;
            }
        }
        else
        {
            Debug.Log("Steps or Picking Steps are null!");}
    }
}
