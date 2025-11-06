package com.example.jwttest;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.*;
import javafx.scene.paint.Color;
import okhttp3.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;
import java.util.ResourceBundle;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class JWTController implements Initializable {

    private static final Logger logger = LoggerFactory.getLogger(JWTController.class);

    // Constants
    private static final String DEFAULT_IP = "localhost";
    private static final String DEFAULT_PORT = "5000";
    private static final int HEALTH_CHECK_INTERVAL = 5;
    private static final int REQUEST_TIMEOUT = 10;
    private static final int HEALTH_TIMEOUT = 5;
    private static final String CONFIG_FILE = "jwt_gui_config.json";

    // Configuration and state
    private Map<String, Object> config;
    private Map<String, String> endpoints;
    private String accessToken = "";
    private String refreshToken = "";
    private String healthStatus = "unknown"; // unknown, checking, healthy, unhealthy

    // HTTP client
    private final OkHttpClient httpClient = new OkHttpClient.Builder()
            .connectTimeout(REQUEST_TIMEOUT, TimeUnit.SECONDS)
            .readTimeout(REQUEST_TIMEOUT, TimeUnit.SECONDS)
            .writeTimeout(REQUEST_TIMEOUT, TimeUnit.SECONDS)
            .build();

    private final ObjectMapper objectMapper = new ObjectMapper();
    private ScheduledExecutorService healthCheckExecutor;

    // FXML injected fields
    @FXML private TextField ipField;
    @FXML private TextField portField;
    @FXML private Button saveConfigButton;
    @FXML private Label statusLabel;
    @FXML private Canvas statusCanvas;
    @FXML private TextField regUsernameField;
    @FXML private TextField regEmailField;
    @FXML private PasswordField regPasswordField;
    @FXML private Button registerButton;
    @FXML private TextField usernameField;
    @FXML private PasswordField passwordField;
    @FXML private Button loginButton;
    @FXML private Button protectedButton;
    @FXML private Button refreshButton;
    @FXML private Button logoutButton;
    @FXML private Button viewUsersButton;
    @FXML private TextField deleteUserField;
    @FXML private Button deleteUserButton;
    @FXML private TableView<User> usersTable;
    @FXML private TableColumn<User, Integer> idColumn;
    @FXML private TableColumn<User, String> usernameColumn;
    @FXML private TableColumn<User, String> emailColumn;
    @FXML private TableColumn<User, String> createdColumn;
    @FXML private TextArea logArea;
    @FXML private Label accessTokenLabel;
    @FXML private Label refreshTokenLabel;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        loadConfig();
        setupTableColumns();
        startHealthCheck();
        updateTokenLabels();
        logMessage("Configuración cargada correctamente");
    }

    private void loadConfig() {
        config = new HashMap<>();
        config.put("ip", DEFAULT_IP);
        config.put("port", DEFAULT_PORT);
        endpoints = Map.of(
                "register", "/register",
                "login", "/login",
                "refresh", "/refresh",
                "logout", "/logout",
                "protected", "/protected",
                "health", "/health",
                "users", "/users",
                "delete_user", "/users/"
        );
        config.put("endpoints", endpoints);

        File configFile = new File(CONFIG_FILE);
        if (configFile.exists()) {
            try {
                String content = Files.readString(configFile.toPath());
                Map<String, Object> loadedConfig = objectMapper.readValue(content, Map.class);
                config.putAll(loadedConfig);
            } catch (IOException e) {
                logMessage("Error loading config file: " + e.getMessage());
            }
        }

        // Update UI fields
        Platform.runLater(() -> {
            ipField.setText((String) config.get("ip"));
            portField.setText((String) config.get("port"));
        });
    }

    private void saveConfig() {
        config.put("ip", ipField.getText());
        config.put("port", portField.getText());

        try {
            String json = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(config);
            Files.writeString(Paths.get(CONFIG_FILE), json);
            logMessage("Configuración guardada");
        } catch (IOException e) {
            logMessage("Error guardando configuración: " + e.getMessage());
        }
    }

    private String getBaseUrl() {
        return "http://" + config.get("ip") + ":" + config.get("port");
    }

    private void setupTableColumns() {
        idColumn.setCellValueFactory(cellData -> cellData.getValue().idProperty().asObject());
        usernameColumn.setCellValueFactory(cellData -> cellData.getValue().usernameProperty());
        emailColumn.setCellValueFactory(cellData -> cellData.getValue().emailProperty());
        createdColumn.setCellValueFactory(cellData -> cellData.getValue().createdAtProperty());
    }

    private void startHealthCheck() {
        healthCheckExecutor = Executors.newSingleThreadScheduledExecutor(r -> {
            Thread t = new Thread(r, "HealthCheck");
            t.setDaemon(true);
            return t;
        });

        healthCheckExecutor.scheduleAtFixedRate(this::checkHealth, 0, HEALTH_CHECK_INTERVAL, TimeUnit.SECONDS);
    }

    private void checkHealth() {
        updateSemaphore("checking");
        String url = getBaseUrl() + endpoints.get("health");

        logMessage("Verificando salud: GET " + url);

        Request request = new Request.Builder()
                .url(url)
                .get()
                .build();

        try (Response response = httpClient.newCall(request).execute()) {
            String responseBody = response.body().string();
            JsonNode jsonNode = objectMapper.readTree(responseBody);

            if (response.isSuccessful() && jsonNode.get("status").asText().equals("healthy")) {
                updateSemaphore("healthy");
                String dbStatus = jsonNode.has("database") ? jsonNode.get("database").asText() : "unknown";
                String redisStatus = jsonNode.has("redis") ? jsonNode.get("redis").asText() : "unknown";
                logMessage("Microservicio saludable - DB: " + dbStatus + ", Redis: " + redisStatus);
            } else {
                updateSemaphore("unhealthy");
                logMessage("Microservicio no saludable - Status: " + response.code());
            }
        } catch (Exception e) {
            updateSemaphore("unhealthy");
            logMessage("Error conectando al microservicio: " + e.getMessage());
        }
    }

    private void updateSemaphore(String status) {
        healthStatus = status;
        Platform.runLater(() -> {
            String statusText;
            Color color;

            switch (status) {
                case "unknown":
                    statusText = "Estado: Desconocido";
                    color = Color.GRAY;
                    break;
                case "checking":
                    statusText = "Estado: Procesando";
                    color = Color.ORANGE;
                    break;
                case "healthy":
                    statusText = "Estado: Saludable";
                    color = Color.GREEN;
                    break;
                case "unhealthy":
                default:
                    statusText = "Estado: No funciona";
                    color = Color.RED;
                    break;
            }

            statusLabel.setText(statusText);

            // Draw circle on canvas
            GraphicsContext gc = statusCanvas.getGraphicsContext2D();
            gc.clearRect(0, 0, statusCanvas.getWidth(), statusCanvas.getHeight());
            gc.setFill(color);
            double centerX = statusCanvas.getWidth() / 2;
            double centerY = statusCanvas.getHeight() / 2;
            double radius = Math.min(centerX, centerY) - 2;
            gc.fillOval(centerX - radius, centerY - radius, radius * 2, radius * 2);
        });
    }

    private void updateTokenLabels() {
        Platform.runLater(() -> {
            accessTokenLabel.setText(maskToken(accessToken));
            refreshTokenLabel.setText(maskToken(refreshToken));
        });
    }

    private String maskToken(String token) {
        return token != null && !token.isEmpty() ? token : "";
    }

    private void logMessage(String message) {
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss"));
        String logEntry = "[" + timestamp + "] " + message;

        Platform.runLater(() -> {
            logArea.appendText(logEntry + "\n");
            // Auto scroll to bottom
            logArea.setScrollTop(Double.MAX_VALUE);
        });

        logger.info(message);
    }

    @FXML
    private void saveConfigButton() {
        saveConfig();
    }

    @FXML
    private void register() {
        String username = regUsernameField.getText();
        String email = regEmailField.getText();
        String password = regPasswordField.getText();

        if (username.isEmpty() || email.isEmpty() || password.isEmpty()) {
            showAlert(Alert.AlertType.ERROR, "Error", "Todos los campos son requeridos");
            return;
        }

        Task<Void> task = new Task<>() {
            @Override
            protected Void call() throws Exception {
                String url = getBaseUrl() + endpoints.get("register");
                Map<String, String> requestBody = Map.of(
                        "username", username,
                        "email", email,
                        "password", password
                );

                String jsonBody = objectMapper.writeValueAsString(requestBody);
                logMessage("Registrando usuario: POST " + url);
                logMessage("Datos enviados: " + jsonBody);

                RequestBody body = RequestBody.create(jsonBody, MediaType.parse("application/json"));
                Request request = new Request.Builder()
                        .url(url)
                        .post(body)
                        .build();

                try (Response response = httpClient.newCall(request).execute()) {
                    String responseBody = response.body().string();

                    if (response.isSuccessful()) {
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        logMessage("Usuario registrado exitosamente - ID: " + jsonNode.get("user_id").asText());
                        Platform.runLater(() -> showAlert(Alert.AlertType.INFORMATION, "Éxito", "Usuario registrado exitosamente"));
                    } else {
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        String errorMessage = jsonNode.has("message") ? jsonNode.get("message").asText() : "Error desconocido";
                        logMessage("Error en registro: " + errorMessage);
                        Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error en registro: " + errorMessage));
                    }
                }
                return null;
            }

            @Override
            protected void failed() {
                Throwable e = getException();
                logMessage("Error de conexión: " + e.getMessage());
                Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error de conexión: " + e.getMessage()));
            }
        };

        new Thread(task).start();
    }

    @FXML
    private void login() {
        String username = usernameField.getText();
        String password = passwordField.getText();

        if (username.isEmpty() || password.isEmpty()) {
            showAlert(Alert.AlertType.ERROR, "Error", "Usuario y contraseña son requeridos");
            return;
        }

        Task<Void> task = new Task<>() {
            @Override
            protected Void call() throws Exception {
                String url = getBaseUrl() + endpoints.get("login");
                Map<String, String> requestBody = Map.of(
                        "username", username,
                        "password", password
                );

                String jsonBody = objectMapper.writeValueAsString(requestBody);
                logMessage("Iniciando sesión: POST " + url);
                logMessage("Datos enviados: " + jsonBody);

                RequestBody body = RequestBody.create(jsonBody, MediaType.parse("application/json"));
                Request request = new Request.Builder()
                        .url(url)
                        .post(body)
                        .build();

                try (Response response = httpClient.newCall(request).execute()) {
                    String responseBody = response.body().string();

                    if (response.isSuccessful()) {
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        accessToken = jsonNode.get("access_token").asText();
                        refreshToken = jsonNode.get("refresh_token").asText();

                        updateTokenLabels();
                        logMessage("Login exitoso");
                        logMessage("Access Token: " + maskToken(accessToken));
                        logMessage("Refresh Token: " + maskToken(refreshToken));
                        Platform.runLater(() -> showAlert(Alert.AlertType.INFORMATION, "Éxito", "Login exitoso"));
                    } else {
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        String errorMessage = jsonNode.has("message") ? jsonNode.get("message").asText() : "Error desconocido";
                        logMessage("Error en login: " + errorMessage);
                        Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error en login: " + errorMessage));
                    }
                }
                return null;
            }

            @Override
            protected void failed() {
                Throwable e = getException();
                logMessage("Error de conexión: " + e.getMessage());
                Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error de conexión: " + e.getMessage()));
            }
        };

        new Thread(task).start();
    }

    @FXML
    private void accessProtected() {
        if (accessToken == null || accessToken.isEmpty()) {
            showAlert(Alert.AlertType.ERROR, "Error", "No hay token de acceso disponible");
            return;
        }

        Task<Void> task = new Task<>() {
            @Override
            protected Void call() throws Exception {
                String url = getBaseUrl() + endpoints.get("protected");

                Request request = new Request.Builder()
                        .url(url)
                        .addHeader("Authorization", "Bearer " + accessToken)
                        .get()
                        .build();

                logMessage("Accediendo endpoint protegido: GET " + url);
                logMessage("Headers: Authorization: Bearer " + maskToken(accessToken));

                try (Response response = httpClient.newCall(request).execute()) {
                    String responseBody = response.body().string();

                    if (response.isSuccessful()) {
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        logMessage("Acceso exitoso al endpoint protegido");
                        logMessage("Respuesta: " + jsonNode.toPrettyString());
                        String message = jsonNode.has("message") ? jsonNode.get("message").asText() : "Acceso concedido";
                        Platform.runLater(() -> showAlert(Alert.AlertType.INFORMATION, "Éxito", "Acceso protegido: " + message));
                    } else {
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        String errorMessage = jsonNode.has("message") ? jsonNode.get("message").asText() : "Error desconocido";
                        logMessage("Error accediendo protegido: " + errorMessage);
                        Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error: " + errorMessage));
                    }
                }
                return null;
            }

            @Override
            protected void failed() {
                Throwable e = getException();
                logMessage("Error de conexión: " + e.getMessage());
                Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error de conexión: " + e.getMessage()));
            }
        };

        new Thread(task).start();
    }

    @FXML
    private void refreshToken() {
        logMessage("Botón Refresh Token presionado");

        if (refreshToken == null || refreshToken.isEmpty()) {
            logMessage("ERROR: No hay refresh token disponible");
            showAlert(Alert.AlertType.ERROR, "Error", "No hay refresh token disponible");
            return;
        }

        logMessage("Refresh token disponible: " + maskToken(refreshToken).substring(0, Math.min(20, refreshToken.length())) + "...");

        Task<Void> task = new Task<>() {
            @Override
            protected Void call() throws Exception {
                String url = getBaseUrl() + endpoints.get("refresh");
                Map<String, String> requestBody = Map.of("refresh_token", refreshToken);

                String jsonBody = objectMapper.writeValueAsString(requestBody);
                logMessage("Enviando solicitud: POST " + url);
                logMessage("Datos enviados: " + jsonBody);

                RequestBody body = RequestBody.create(jsonBody, MediaType.parse("application/json"));
                Request request = new Request.Builder()
                        .url(url)
                        .post(body)
                        .build();

                try (Response response = httpClient.newCall(request).execute()) {
                    logMessage("Respuesta recibida - Status: " + response.code());

                    if (response.isSuccessful()) {
                        String responseBody = response.body().string();
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        accessToken = jsonNode.get("access_token").asText();

                        updateTokenLabels();
                        logMessage("Token refrescado exitosamente");
                        logMessage("Nuevo Access Token: " + maskToken(accessToken).substring(0, Math.min(20, accessToken.length())) + "...");
                        Platform.runLater(() -> showAlert(Alert.AlertType.INFORMATION, "Éxito", "Token refrescado exitosamente"));
                    } else {
                        String responseBody = response.body().string();
                        try {
                            JsonNode jsonNode = objectMapper.readTree(responseBody);
                            String errorMessage = jsonNode.has("message") ? jsonNode.get("message").asText() : "Error desconocido";
                            logMessage("Error del servidor: " + errorMessage);
                            Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error: " + errorMessage));
                        } catch (Exception e) {
                            logMessage("Error HTTP: " + response.code() + " - " + responseBody);
                            Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error HTTP: " + response.code() + ". Respuesta no es JSON."));
                        }
                    }
                } catch (IOException e) {
                    if (e.getMessage().contains("timeout")) {
                        logMessage("ERROR: Timeout conectando al microservicio");
                        Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Timeout: El microservicio no responde"));
                    } else {
                        throw e;
                    }
                }
                return null;
            }

            @Override
            protected void failed() {
                Throwable e = getException();
                if (e instanceof java.net.ConnectException) {
                    logMessage("ERROR: No se puede conectar al microservicio");
                    Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error de conexión: Verifica que el microservicio esté ejecutándose"));
                } else {
                    logMessage("ERROR inesperado: " + e.getMessage());
                    Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error inesperado: " + e.getMessage()));
                }
            }
        };

        new Thread(task).start();
    }

    @FXML
    private void logout() {
        if (accessToken == null || accessToken.isEmpty()) {
            showAlert(Alert.AlertType.ERROR, "Error", "No hay token de acceso disponible");
            return;
        }

        Task<Void> task = new Task<>() {
            @Override
            protected Void call() throws Exception {
                String url = getBaseUrl() + endpoints.get("logout");

                Request request = new Request.Builder()
                        .url(url)
                        .addHeader("Authorization", "Bearer " + accessToken)
                        .post(RequestBody.create("", null))
                        .build();

                logMessage("Cerrando sesión: POST " + url);
                logMessage("Headers: Authorization: Bearer " + maskToken(accessToken));

                try (Response response = httpClient.newCall(request).execute()) {
                    if (response.isSuccessful()) {
                        // Clear tokens
                        accessToken = "";
                        refreshToken = "";
                        updateTokenLabels();

                        logMessage("Sesión cerrada exitosamente");
                        Platform.runLater(() -> showAlert(Alert.AlertType.INFORMATION, "Éxito", "Sesión cerrada exitosamente"));
                    } else {
                        String responseBody = response.body().string();
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        String errorMessage = jsonNode.has("message") ? jsonNode.get("message").asText() : "Error desconocido";
                        logMessage("Error en logout: " + errorMessage);
                        Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error: " + errorMessage));
                    }
                }
                return null;
            }

            @Override
            protected void failed() {
                Throwable e = getException();
                logMessage("Error de conexión: " + e.getMessage());
                Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error de conexión: " + e.getMessage()));
            }
        };

        new Thread(task).start();
    }

    @FXML
    private void getUsers() {
        if (accessToken == null || accessToken.isEmpty()) {
            showAlert(Alert.AlertType.ERROR, "Error", "Debes estar autenticado para ver usuarios");
            return;
        }

        Task<Void> task = new Task<>() {
            @Override
            protected Void call() throws Exception {
                String url = getBaseUrl() + endpoints.get("users");

                Request request = new Request.Builder()
                        .url(url)
                        .addHeader("Authorization", "Bearer " + accessToken)
                        .get()
                        .build();

                logMessage("Obteniendo lista de usuarios: GET " + url);

                try (Response response = httpClient.newCall(request).execute()) {
                    String responseBody = response.body().string();

                    if (response.isSuccessful()) {
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        JsonNode usersArray = jsonNode.get("users");

                        ObservableList<User> users = FXCollections.observableArrayList();
                        for (JsonNode userNode : usersArray) {
                            User user = new User(
                                    userNode.get("id").asInt(),
                                    userNode.get("username").asText(),
                                    userNode.get("email").asText(),
                                    userNode.get("created_at").asText()
                            );
                            users.add(user);
                        }

                        Platform.runLater(() -> {
                            usersTable.setItems(users);
                            showAlert(Alert.AlertType.INFORMATION, "Éxito", "Usuarios obtenidos: " + users.size());
                        });

                        logMessage("Usuarios obtenidos: " + users.size() + " usuarios");
                    } else {
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        String errorMessage = jsonNode.has("message") ? jsonNode.get("message").asText() : "Error desconocido";
                        logMessage("Error obteniendo usuarios: " + errorMessage);
                        Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error: " + errorMessage));
                    }
                }
                return null;
            }

            @Override
            protected void failed() {
                Throwable e = getException();
                logMessage("Error de conexión: " + e.getMessage());
                Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error de conexión: " + e.getMessage()));
            }
        };

        new Thread(task).start();
    }

    @FXML
    private void deleteUser() {
        if (accessToken == null || accessToken.isEmpty()) {
            showAlert(Alert.AlertType.ERROR, "Error", "Debes estar autenticado para eliminar usuarios");
            return;
        }

        String userId = deleteUserField.getText();
        if (userId.isEmpty()) {
            showAlert(Alert.AlertType.ERROR, "Error", "Ingresa el ID del usuario a eliminar");
            return;
        }

        Task<Void> task = new Task<>() {
            @Override
            protected Void call() throws Exception {
                String url = getBaseUrl() + endpoints.get("delete_user") + userId;

                Request request = new Request.Builder()
                        .url(url)
                        .addHeader("Authorization", "Bearer " + accessToken)
                        .delete()
                        .build();

                logMessage("Eliminando usuario " + userId + ": DELETE " + url);

                try (Response response = httpClient.newCall(request).execute()) {
                    if (response.isSuccessful()) {
                        String responseBody = response.body().string();
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        logMessage("Usuario " + userId + " eliminado exitosamente");
                        Platform.runLater(() -> {
                            showAlert(Alert.AlertType.INFORMATION, "Éxito", "Usuario eliminado exitosamente");
                            deleteUserField.clear();
                            getUsers(); // Refresh user list
                        });
                    } else {
                        String responseBody = response.body().string();
                        JsonNode jsonNode = objectMapper.readTree(responseBody);
                        String errorMessage = jsonNode.has("message") ? jsonNode.get("message").asText() : "Error desconocido";
                        logMessage("Error eliminando usuario: " + errorMessage);
                        Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error: " + errorMessage));
                    }
                }
                return null;
            }

            @Override
            protected void failed() {
                Throwable e = getException();
                logMessage("Error de conexión: " + e.getMessage());
                Platform.runLater(() -> showAlert(Alert.AlertType.ERROR, "Error", "Error de conexión: " + e.getMessage()));
            }
        };

        new Thread(task).start();
    }

    private void showAlert(Alert.AlertType type, String title, String message) {
        Alert alert = new Alert(type);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    // User model class
    public static class User {
        private final javafx.beans.property.IntegerProperty id = new javafx.beans.property.SimpleIntegerProperty();
        private final javafx.beans.property.StringProperty username = new javafx.beans.property.SimpleStringProperty();
        private final javafx.beans.property.StringProperty email = new javafx.beans.property.SimpleStringProperty();
        private final javafx.beans.property.StringProperty createdAt = new javafx.beans.property.SimpleStringProperty();

        public User(int id, String username, String email, String createdAt) {
            setId(id);
            setUsername(username);
            setEmail(email);
            setCreatedAt(createdAt);
        }

        public int getId() { return id.get(); }
        public void setId(int id) { this.id.set(id); }
        public javafx.beans.property.IntegerProperty idProperty() { return id; }

        public String getUsername() { return username.get(); }
        public void setUsername(String username) { this.username.set(username); }
        public javafx.beans.property.StringProperty usernameProperty() { return username; }

        public String getEmail() { return email.get(); }
        public void setEmail(String email) { this.email.set(email); }
        public javafx.beans.property.StringProperty emailProperty() { return email; }

        public String getCreatedAt() { return createdAt.get(); }
        public void setCreatedAt(String createdAt) { this.createdAt.set(createdAt); }
        public javafx.beans.property.StringProperty createdAtProperty() { return createdAt; }
    }
}