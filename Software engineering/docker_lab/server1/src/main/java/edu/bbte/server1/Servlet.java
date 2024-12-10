package edu.bbte.server1;


import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.ServletConfig;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

@WebServlet("/authors/*")
public class Servlet extends HttpServlet {
    private ObjectMapper objectMapper;
    private Connection connection;

    @Override
    public void init(ServletConfig config) throws ServletException {
        try {
            objectMapper = new ObjectMapper();
            Class.forName("com.mysql.cj.jdbc.Driver");
            connection = DriverManager.getConnection(System.getenv("JDBC_URL"));
        } catch (ClassNotFoundException | SQLException e) {
            throw new ServletException(e);
        }
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        try {
            resp.setHeader("Content-Type", "application/json");
            String pathInfo = req.getPathInfo();
            if (pathInfo == null || pathInfo.equals("/")) {
                Statement statement = connection.createStatement();
                ResultSet resultSet = statement.executeQuery("SELECT * FROM Author");
                List<Author> list = new ArrayList<>();
                while (resultSet.next()){
                    list.add(new Author(resultSet.getLong(1), resultSet.getString(2)));
                }
                objectMapper.writeValue(resp.getOutputStream(), list);
                return;
            }
            String id = pathInfo.split("/")[1];
            PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM Author WHERE authorID = ?");
            preparedStatement.setString(1, id);
            ResultSet resultSet = preparedStatement.executeQuery();
            List<Author> list = new ArrayList<>();
            if (resultSet.next()){
                list.add(new Author(resultSet.getLong(1), resultSet.getString(2)));
            }
            objectMapper.writeValue(resp.getOutputStream(), list);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
