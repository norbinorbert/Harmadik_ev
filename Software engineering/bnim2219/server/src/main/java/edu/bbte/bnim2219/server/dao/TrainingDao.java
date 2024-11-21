package edu.bbte.bnim2219.server.dao;

import edu.bbte.bnim2219.server.model.Training;

import java.util.Collection;

public interface TrainingDao {
    void create(Training training);

    Training findById(Long id);

    Collection<Training> findAll();
}
