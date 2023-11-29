using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class TimeManager : MonoBehaviour
{
    public static Action FiveSecondRule;
    public static Action OnMinuteChanged;
    public static Action OnHourChanged;
    public static int Minute{get; private set;}
    public static int Hour{get;private set;}

    private float timer;
    private float minuteToRealTime = 1f;

    void Start()
    {
        Minute = 0;
        Hour = 0;
        timer = minuteToRealTime;
    }

    void Update()
    {
        timer -= Time.deltaTime;

        if(timer <= 0)
        {
            Minute++;
            OnMinuteChanged?.Invoke();

            if(Minute >= 59)
            {
                Hour++;
                OnHourChanged?.Invoke();
                Minute = 0;
            }

            timer = minuteToRealTime;
        }
    }
}
