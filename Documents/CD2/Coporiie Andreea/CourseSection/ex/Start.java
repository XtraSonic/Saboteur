import java.util.Scanner;

public class Start {

    private static CourseSection courseSection;


    public static void main(String[] args) {
        boolean quit = false;
        Scanner keyboard = new Scanner(System.in);
        System.out.println("CourseSection test");
        while (!quit){
            String command = keyboard.nextLine();
            if (command.matches("#quit")){
                quit = true;
            }
            if (command.matches("#new")){
                System.out.println(">Create new course");
                System.out.println(">Enter name:");
                String courseName = keyboard.nextLine();
                System.out.println(">Enter min number of students");
                int minStudents = keyboard.nextInt();
                System.out.println(">Enter max number of students");
                int maxStudents = keyboard.nextInt();
                Course course = new Course(courseName, minStudents, maxStudents);
                courseSection = new CourseSection(course);
                System.out.println(courseSection.getState());
            }
            if (command.matches("#open")){
                courseSection.openRegistration();
                System.out.println(courseSection.getState());
            }
            if (command.matches("#close")){
                courseSection.closeRegistration();
                System.out.println(courseSection.getState());
            }
            if (command.matches("#cancel")){
                courseSection.cancel();
                System.out.println(courseSection.getState());
            }
            if (command.matches("#register")){
                System.out.println(">Register new student");
                System.out.println(">Enter student name:");
                String studentName = keyboard.nextLine();
                Student student = new Student(studentName);
                System.out.println(">Requesting to register " + studentName);
                courseSection.requestToRegister(student);
                System.out.println(courseSection.getState());
            }
        }
    }

}
