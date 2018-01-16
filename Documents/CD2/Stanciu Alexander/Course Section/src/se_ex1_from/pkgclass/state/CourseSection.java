package se_ex1_from.pkgclass.state;

import java.util.ArrayList;
import java.util.List;

public class CourseSection
{
    private Course course; // A many-to-one relation with Course
    private final List<Registration> registrationList; // A one-to-many relation with Registration
    private final String name;
    
    private boolean closed;
    private boolean canceled;
    private boolean opened;

    public CourseSection(String name, Course c)
    {
        registrationList= new ArrayList<>();
        course=c;
        this.name=name;
    }

    public String getName() {
        return name;
    }

    public boolean requestToRegister(Registration r)
    {
        if(opened && r.meets(course.getPrerequisites())) {
            this.addToRegistrationList(r);
            return true;
        }
        return false;
    }

    public void addToRegistrationList(Registration r)
    {
        registrationList.add(r);
        if(registrationList.size()>=course.getMax())
        {
            this.closed=true;
            this.opened =  false;
        }
            
    }


    public void openRegistration()
    {
        opened = true;
    }

    public void cancel()
    {
        canceled = true;
        opened = false;
        
        registrationList.clear();
    }

    public void closeRegistration()
    {
        if(registrationList.size()<course.getMinimum())
        {
           this.cancel();
        }
        else
        {
            closed = true;
            opened = false;
        }
    }
    public String getState()
    {

        if(opened)
        {
            if(registrationList.size()<course.getMinimum())
                return "NotEnoughStudents";
            else
                return "EnoughStudents";
        }
        else
        {
            if(closed&&!canceled)
                return "Closed";

            if(canceled)
                return "Canceled";

            return "Planned";
        }
    }

}
