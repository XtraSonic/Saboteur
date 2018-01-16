public class Course {

    private int minNumber;
    private int maxNumber;

    private String name;

    public Course(String name, int minNumber, int maxNumber) {
        this.name = name;
        this.minNumber = minNumber;
        this.maxNumber = maxNumber;
    }

    public int getMinNumber(){
        return this.minNumber;
    }

    public int getMaxNumber() {
        return maxNumber;
    }

    public String getName() {
        return name;
    }
}
