package edu.bbte.bnim2219.server.model;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.sql.Time;

@Data
@AllArgsConstructor
public class Training {
    private Long trainingId;
    private Time duration;
    private Boolean complete;

    public boolean isTrainingComplete() {
        return complete;
    }
}