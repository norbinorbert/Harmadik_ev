package edu.bbte.bnim2219.client;

import edu.bbte.bnim2219.server.dao.DaoFactory;
import edu.bbte.bnim2219.server.dao.TrainingDao;
import edu.bbte.bnim2219.server.model.Training;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.sql.Time;

public class Main {
    private static final TrainingDao trainingDao = DaoFactory.getInstance().getTrainingDao();
    private static final BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
    private static final Logger log = LoggerFactory.getLogger(Main.class);

    private static void createTraining() throws IOException {
        while (true) {
            try {
                String input;
                System.out.println("Please provide an ID for the training: ");
                input = bufferedReader.readLine();
                final long id = Long.parseLong(input);

                System.out.println("Tell me the time the training will take");
                System.out.println("Hours: ");
                input = bufferedReader.readLine();
                final long hours = Long.parseLong(input);

                System.out.println("Minutes: ");
                input = bufferedReader.readLine();
                final long minutes = Long.parseLong(input);

                System.out.println("Seconds: ");
                input = bufferedReader.readLine();
                final long seconds = Long.parseLong(input);

                long milliseconds = hours * 3600000 + minutes * 60000 + seconds * 1000;
                final Time time = new Time(milliseconds);

                System.out.println("If the training is done already, please type \"y\": ");
                input = bufferedReader.readLine();
                if (input == null) {
                    continue;
                }
                trainingDao.create(new Training(id, time, input.equals("y")));
                break;
            } catch (NumberFormatException e) {
                System.out.println("Please provide a number. Restarting action");
            }
        }
    }

    private static void listAllTrainings() {
        log.info("Listed all trainings");
        var trainings = trainingDao.findAll();
        if (trainings.isEmpty()) {
            System.out.println("No trainings to show.");
        } else {
            trainings.forEach((training -> System.out.println("ID: " + training.getTrainingId()
                    + " Duration: " + training.getDuration().getTime() + "ms"
                    + " Done: " + training.getComplete())));
        }
    }

    private static void listTrainingByID() throws IOException {
        while (true) {
            String input;
            System.out.println("ID:");
            try {
                input = bufferedReader.readLine();
                var training = trainingDao.findById(Long.parseLong(input));
                if (training == null) {
                    System.out.println("No training with that ID");
                } else {
                    System.out.println("ID: " + training.getTrainingId()
                            + " Duration: " + training.getDuration().getTime() + "ms"
                            + " Done: " + training.getComplete());
                }
                break;
            } catch (NumberFormatException e) {
                System.out.println("Please provide a number");
            }
        }
    }

    public static void main(String[] args) {
        label:
        while (true) {
            System.out.println("Options:");
            System.out.println("1. Create new training");
            System.out.println("2. List all trainings");
            System.out.println("3. Find training by id");
            System.out.println("0. End program");

            String input;
            try {
                input = bufferedReader.readLine();
                if (input == null) {
                    continue;
                }
                switch (input) {
                    case "0":
                        System.out.println("Goodbye");
                        break label;
                    case "1":
                        createTraining();
                        break;
                    case "2":
                        listAllTrainings();
                        break;
                    case "3":
                        listTrainingByID();
                        break;
                    default:
                        System.out.println("Option doesn't exist");
                        break;
                }
            } catch (IOException e) {
                System.out.println("Unexpected error, going back to options page");
            }
        }
    }
}
