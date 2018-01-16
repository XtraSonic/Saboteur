public class Registration {

    private CourseSection courseSection;
    private Student student;

    public Registration(CourseSection courseSection, Student student) {
        this.courseSection = courseSection;
        this.student = student;
        this.student.addRegistration(this);
    }
}
