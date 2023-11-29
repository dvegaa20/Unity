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
            foreach (Step step in steps)
            {
                foreach (PickingSteps pickingStep in pickingSteps)
                {
                    if (StepCountManager.Instance.GetCurrentStepCount() == pickingStep.step)
                    {
                        if (other.gameObject.CompareTag("Food"))
                        {
                            Destroy(other.gameObject);
                        }
                    }
                }
            }
        }
        else
        {
            Debug.Log("Steps or Picking Steps are null!");
        }
    }
}
