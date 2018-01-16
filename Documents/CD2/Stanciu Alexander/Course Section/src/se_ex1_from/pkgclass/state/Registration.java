package se_ex1_from.pkgclass.state;

import java.util.List;

public class Registration
{
    private final Student student;
    private final CourseSection courseSection;

    public Registration(Student student,CourseSection courseSection)
    {
        this.student = student;
        this.courseSection=courseSection;
    }

    public boolean meets(List<String> prerequisite) {
        return prerequisite.stream().noneMatch((elementRequired) -> (student.knows(elementRequired) == false));
    }
}
