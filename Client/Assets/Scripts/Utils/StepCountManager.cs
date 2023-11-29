using UnityEngine;

public class StepCountManager : MonoBehaviour
{
    private int currentStepCount;
    private static StepCountManager _instance;
    public static StepCountManager Instance
    {
        get { return _instance; }
    }

    public int GetCurrentStepCount()
    {
        return currentStepCount;
    }

    public void IncrementStepCount()
    {
        currentStepCount++;
    }

    void Awake()
    {
        _instance = this;
    }
}
