package com.uav.cursos;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.Contact;

/**
 * API REST - Sistema de Cursos
 * Universidad Autonoma Veracruzana
 * Arquitectura Orientada a Servicios
 *
 * Esta aplicacion implementa una API RESTful para la gestion
 * de cursos academicos utilizando Spring Boot y MySQL.
 */
@SpringBootApplication
@OpenAPIDefinition(
    info = @Info(
        title = "API REST - Sistema de Cursos UAV",
        version = "1.0.0",
        description = "API RESTful para la gestion de cursos academicos de la Universidad Autonoma Veracruzana",
        contact = @Contact(
            name = "Universidad Autonoma Veracruzana",
            email = "soporte@uav.mx"
        )
    )
)
public class CursosApiApplication {

    public static void main(String[] args) {
        System.out.println("============================================");
        System.out.println("API REST - SISTEMA DE CURSOS");
        System.out.println("Universidad Autonoma Veracruzana");
        System.out.println("============================================");
        SpringApplication.run(CursosApiApplication.class, args);
        System.out.println("\nServidor iniciado en http://localhost:8080");
        System.out.println("Swagger UI: http://localhost:8080/swagger-ui.html");
        System.out.println("API Docs: http://localhost:8080/api-docs");
        System.out.println("============================================");
    }
}
