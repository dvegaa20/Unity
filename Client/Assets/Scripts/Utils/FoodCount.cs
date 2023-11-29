using TMPro;
using UnityEngine;

public class FoodCount : MonoBehaviour
{
    public TextMeshProUGUI foodTextMesh;
    private int foodCount;

    public int GetActiveFoodCount()
    {
        int count = 0;
        GameObject[] foods = GameObject.FindGameObjectsWithTag("Food");
        foreach (GameObject food in foods)
        {
            count++;
        }
        return count;
    }

    void Update()
    {
        if (foodTextMesh != null)
        {
            foodCount = GetActiveFoodCount();
            
            if (foodCount>= 0)
            {
                foodTextMesh.text = "Current Food: " + foodCount.ToString();
            }
            else
            {
                foodTextMesh.text = "Current Food: 00";
            }
        }
    }
}