package com.uav.cursos.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

/**
 * Entidad Curso
 * Representa un curso academico en el sistema
 */
@Entity
@Table(name = "cursos")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Curso {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_curso")
    private Long idCurso;

    @NotBlank(message = "El codigo del curso es obligatorio")
    @Size(max = 20, message = "El codigo no puede exceder 20 caracteres")
    @Column(name = "codigo", unique = true, nullable = false, length = 20)
    private String codigo;

    @NotBlank(message = "El nombre del curso es obligatorio")
    @Size(max = 150, message = "El nombre no puede exceder 150 caracteres")
    @Column(name = "nombre", nullable = false, length = 150)
    private String nombre;

    @Column(name = "descripcion", columnDefinition = "TEXT")
    private String descripcion;

    @NotNull(message = "Los creditos son obligatorios")
    @Min(value = 1, message = "El curso debe tener al menos 1 credito")
    @Max(value = 20, message = "El curso no puede tener mas de 20 creditos")
    @Column(name = "creditos", nullable = false)
    private Integer creditos;

    @Min(value = 0, message = "Las horas teoricas no pueden ser negativas")
    @Column(name = "horas_teoricas")
    private Integer horasTeoricas = 0;

    @Min(value = 0, message = "Las horas practicas no pueden ser negativas")
    @Column(name = "horas_practicas")
    private Integer horasPracticas = 0;

    @Column(name = "id_carrera")
    private Long idCarrera;

    @Min(value = 1, message = "El semestre debe ser al menos 1")
    @Max(value = 12, message = "El semestre no puede ser mayor a 12")
    @Column(name = "semestre")
    private Integer semestre;

    @Column(name = "estatus", length = 20)
    @Enumerated(EnumType.STRING)
    private EstatusCurso estatus = EstatusCurso.activo;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    public enum EstatusCurso {
        activo,
        inactivo
    }
}
