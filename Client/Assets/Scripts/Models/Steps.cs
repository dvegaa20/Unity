using System.Collections.Generic;

[System.Serializable]

public class Steps {

    public DepositLocation deposit_location;
    public List<Step> steps;
    public List<PickingSteps> picking_steps;

}

[System.Serializable]
public class Step 
{
    public int id;
    public List<Agent> agents;
    public List<Food> food;
}

[System.Serializable]
public class Agent 
{
    public string id;
    public int x;
    public int y;
    public string type;
}

[System.Serializable]
public class Food 
{
    public int x;
    public int y;
}

[System.Serializable]
public class DepositLocation
{
    public float x;
    public float y;
}

[System.Serializable]
public class PickingSteps
{
    public int id_collector;
    public float x;
    public float y;
    public float step;
    public bool picked;
}