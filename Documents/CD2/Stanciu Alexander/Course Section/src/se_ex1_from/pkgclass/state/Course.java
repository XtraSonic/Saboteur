package se_ex1_from.pkgclass.state;

import java.util.List;

public class Course {

    private int minimum;
    private int max;
    private final String name;
    private final List<String> prerequisites;

    public Course(String name, int minimum, int max, List prerequisites) {
        this.name = name;
        if (minimum < max) {
            this.minimum = minimum;

            this.max = max;
        } else {
            this.minimum = max;

            this.max = minimum;
        }
        this.prerequisites = prerequisites;
    }

    public int getMinimum() {
        return minimum;
    }

    @Override
    public String toString() {
        return "Course{" + "minimum=" + minimum + ", name=" + name + ", prerequisites=" + prerequisites + '}';
    }

    public String getName() {
        return name;
    }

    public List<String> getPrerequisites() {
        return prerequisites;
    }

    int getMax() {
        return max;
    }

}
