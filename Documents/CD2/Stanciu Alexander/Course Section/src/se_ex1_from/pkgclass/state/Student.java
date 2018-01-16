package se_ex1_from.pkgclass.state;

import java.util.List;

public class Student
{
    private final String name;
    private final List<String> knowledge;
    

    public Student(String name, List knowledge)
    {
        this.name=name;
        this.knowledge=knowledge;
    }

    public void addToSchedule()
    {


    }

    public boolean hasPassedCourse()
    {

        return false;
    }


    public boolean knows(String elementRequired)
    {
        return knowledge.contains(elementRequired);
    }

    public String getName() {
        return name;
    }
    
}
