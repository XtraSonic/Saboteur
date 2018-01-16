import java.util.ArrayList;
import java.util.List;

public class Student {

    private String name;

    private List<Registration> registrations;

    public Student(String name) {
        this.name = name;
        this.registrations = new ArrayList<>(0);
    }

    @Override
    public String toString() {
        return name;
    }

    public void addRegistration(Registration registration){
        this.registrations.add(registration);
    }
}
