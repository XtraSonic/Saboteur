import java.util.ArrayList;
import java.util.List;

public class CourseSection {

    private boolean open;
    private boolean closedOrCancelled;

    private Course course; //Many-to-one relation with Course
    private List<Registration> registrations; //One-to-many relation with Registration

    public CourseSection(Course course) {
        this.course = course;
        this.open = false;
        this.closedOrCancelled = false;
        this.registrations = new ArrayList<>(0);
    }

    public void openRegistration(){
        this.open = true;
        this.registrations = new ArrayList<>(0);
    }

    public void closeRegistration(){
        this.closedOrCancelled = true;
    }

    public void cancel(){
        if (!this.open || this.closedOrCancelled) {
            System.err.println("Cannot cancel course section");
            return;
        }
        this.closedOrCancelled = true;
        this.registrations.clear();

    }

    public void requestToRegister(Student student){
        if (!this.open || this.closedOrCancelled){
            System.err.println("Cannot register student");
            return;
        }
        Registration newRegistration = new Registration(this, student);
        this.registrations.add(newRegistration);
        if (this.registrations.size() >= this.course.getMaxNumber()){
            this.closedOrCancelled = true;
        }
    }

    public String getState(){
        if (!this.open && !this.closedOrCancelled){
            return "Planned";
        }
        if (this.open){
            if (!this.closedOrCancelled) {
                if (this.registrations.size() < this.course.getMinNumber()) {
                    return "Open - Not Enough Students";
                } else {
                    return "Open - Enough Students";
                }
            }
            else {
                if (this.registrations.size() == 0){
                    return "Canceled";
                }
            }
        }
        return "Closed";
    }

}
