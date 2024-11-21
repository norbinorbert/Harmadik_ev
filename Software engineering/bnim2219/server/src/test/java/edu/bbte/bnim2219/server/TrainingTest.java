package edu.bbte.bnim2219.server;

import edu.bbte.bnim2219.server.model.Training;
import org.junit.jupiter.api.Test;

import java.sql.Time;

public class TrainingTest {

    @Test
    public void testFunction() {
        Training training = new Training(1L, new Time(5), true);
        assert training.isTrainingComplete();
    }
}
