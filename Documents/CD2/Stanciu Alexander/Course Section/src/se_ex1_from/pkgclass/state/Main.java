/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package se_ex1_from.pkgclass.state;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

/**
 *
 * @author Xtra Sonic
 */
public class Main {

    public static String command = new String();
    public static Scanner in = new Scanner(System.in);
    private static List<Student> studentList = new ArrayList<>();
    private static List<Course> courseList = new ArrayList<>();
    private static List<CourseSection> courseSectionList = new ArrayList<>();

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        CourseSection cs = null;

        while (!(command.equals("exit") || command.equals("0"))) {
            System.out.println("\nInput command");
            command = in.next();

            switch (command.toLowerCase()) {
                case "c_c":
                case "c_course":
                    courseList.add(createCourse());
                    break;

                case "c_cs":
                case "c_coursesection":
                    cs = createCourseSection();
                    courseSectionList.add(cs);
                    break;

                case "c_s":
                case "c_student":
                    studentList.add(createStudent());
                    break;

                case "c_r":
                case "c_registration":
                    createRegistration();
                    break;

                case "s":
                case "state":
                    if (cs == null) {
                        System.out.println("Current course section was not initialized");
                        break;
                    }
                    System.out.println("The state of " + cs.getName() + " is " + cs.getState());
                    break;

                case "cs":
                case "change cs":
                    cs = getCourseSectionFromList();
                    break;

                case "o":
                case "open":
                    if (cs == null) {
                        System.out.println("Current course section was not initialized");
                        break;
                    }
                    cs.openRegistration();
                    break;

                case "c":
                case "cancel":
                    if (cs == null) {
                        System.out.println("Current course section was not initialized");
                        break;
                    }
                    cs.cancel();
                    break;
                    
                case "cl":
                case "close":
                    if (cs == null) {
                        System.out.println("Current course section was not initialized");
                        break;
                    }
                    cs.closeRegistration();
                    break;
                    
                case "d":
                case "initialize demo":
                    Course c1 = new Course("c1",
                            2,
                            3,
                            new ArrayList<>(Arrays.asList("p1", "p2"))
                    );
                    Course c2 = new Course("c2",
                            3,
                            3,
                            new ArrayList<>(Arrays.asList("p1", "p3"))
                    );
                    courseList.add(c1);
                    courseList.add(c2);

                    CourseSection cs11 = new CourseSection("cs11", c1);
                    cs = cs11;
                    CourseSection cs12 = new CourseSection("cs12", c1);

                    CourseSection cs21 = new CourseSection("cs21", c2);
                    CourseSection cs22 = new CourseSection("cs22", c2);
                    CourseSection cs23 = new CourseSection("cs23", c2);

                    courseSectionList.add(cs11);
                    courseSectionList.add(cs12);

                    courseSectionList.add(cs21);
                    courseSectionList.add(cs22);
                    courseSectionList.add(cs23);

                    Student s1 = new Student("s1",
                            new ArrayList<>(Arrays.asList("p1", "p2"))
                    );
                    Student s2 = new Student("s2",
                            new ArrayList<>(Arrays.asList("p1", "p3"))
                    );
                    Student s3 = new Student("s3",
                            new ArrayList<>(Arrays.asList("p1", "p2"))
                    );
                    Student s4 = new Student("s4",
                            new ArrayList<>(Arrays.asList("p1", "p3"))
                    );
                    Student s5 = new Student("s5",
                            new ArrayList<>(Arrays.asList("p1", "p2", "p3"))
                    );
                    Student s6 = new Student("s6",
                            new ArrayList<>(Arrays.asList("p1", "p2", "p3"))
                    );

                    studentList.add(s1);
                    studentList.add(s2);
                    studentList.add(s3);
                    studentList.add(s4);
                    studentList.add(s5);
                    studentList.add(s6);

                    break;

                case "0":
                case "exit":
                    System.out.println("Exiting program...");
                    break;

                default:
                    System.out.println("Invalid command");
            }

        }
    }

    private static Course createCourse() {
        System.out.println("Course name:");
        String name = in.next();

        System.out.println("Minimum amount of students:");
        int min = in.nextInt();
        System.out.println("Maximum amount of students:");
        int max = in.nextInt();

        System.out.println("Prerequisits (end with \"\\0\"):");
        ArrayList<String> prq = new ArrayList<>();
        String element = in.next();
        while (!element.equals("\\0")) {
            prq.add(element);
            element = in.next();
        }
        return new Course(name, min,max, prq);
    }

    private static Student createStudent() {
        System.out.println("Student name:");
        String name = in.next();

        System.out.println("Knowledge (end with \"\\0\"):");
        ArrayList<String> knowledge = new ArrayList<>();
        String element = in.next();
        while (!element.equals("\\0")) {
            knowledge.add(element);
            element = in.next();
        }

        return new Student(name, knowledge);

    }

    private static Registration createRegistration() {
        System.out.println("Name of the student to register:");
        String name = in.next();
        Student s = findStudent(name);
        while (s == null && !name.equals("\\0")) {
            System.out.println("Student does not exist, try again (\"\\0\" to quit)");
            name = in.next();
            s = findStudent(name);
        }

        System.out.println("Find a cours section to register him in:");
        CourseSection cs = getCourseSectionFromList();

        if (cs == null || s == null) {
            return null;
        }

        Registration registration = new Registration(s, cs);

        if (cs.requestToRegister(registration)) {
            System.out.println("Registration succesfull");
            return registration;
        } else {
            System.out.println("Registration failed, course section is not opened or " + s.getName() + " lacks the knowdlege required to enter the course section " + cs.getName());
            return null;
        }

    }

    private static CourseSection createCourseSection() {

        System.out.println("Find the cours to which this section belongs:");
        Course c = getCourseFromList();

        System.out.println("Name of the cours to which this section belongs:");
        String name = in.next();
        return new CourseSection(name, c);
    }

    private static Course findCourse(String name) {
        for (Course c : courseList) {
            if (c.getName().equals(name)) {
                return c;
            }
        }
        return null;
    }

    private static Student findStudent(String name) {
        for (Student s : studentList) {
            if (s.getName().equals(name)) {
                return s;
            }
        }
        return null;

    }

    private static CourseSection findCourseSection(String name) {
        for (CourseSection cs : courseSectionList) {
            if (cs.getName().equals(name)) {
                return cs;
            }
        }
        return null;
    }

    private static CourseSection getCourseSectionFromList() {
        System.out.println("Name of the cours section to find:");
        String name = in.next();
        CourseSection cs = findCourseSection(name);
        while (cs == null && !name.equals("\\0")) {
            System.out.println("CourseSection does not exist, try again (\"\\0\" to quit)");
            name = in.next();
            cs = findCourseSection(name);
        }
        return cs;
    }

    private static Course getCourseFromList() {
        System.out.println("Name of the cours to find:");
        String name = in.next();
        Course c = findCourse(name);
        while (c == null && !name.equals("\\0")) {
            System.out.println("Course does not exist, try again (\"\\0\" to quit)");
            name = in.next();
            c = findCourse(name);
        }
        return c;
    }

}
