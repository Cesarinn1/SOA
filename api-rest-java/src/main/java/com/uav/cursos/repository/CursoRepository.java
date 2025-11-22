package com.uav.cursos.repository;

import com.uav.cursos.model.Curso;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * Repositorio para la entidad Curso
 * Proporciona operaciones CRUD y consultas personalizadas
 */
@Repository
public interface CursoRepository extends JpaRepository<Curso, Long> {

    /**
     * Busca un curso por su codigo unico
     */
    Optional<Curso> findByCodigo(String codigo);

    /**
     * Busca cursos por carrera
     */
    List<Curso> findByIdCarrera(Long idCarrera);

    /**
     * Busca cursos por semestre
     */
    List<Curso> findBySemestre(Integer semestre);

    /**
     * Busca cursos por estatus
     */
    List<Curso> findByEstatus(Curso.EstatusCurso estatus);

    /**
     * Busca cursos por carrera y semestre
     */
    List<Curso> findByIdCarreraAndSemestre(Long idCarrera, Integer semestre);

    /**
     * Busca cursos que contengan el nombre especificado
     */
    @Query("SELECT c FROM Curso c WHERE LOWER(c.nombre) LIKE LOWER(CONCAT('%', :nombre, '%'))")
    List<Curso> findByNombreContaining(@Param("nombre") String nombre);

    /**
     * Cuenta cursos activos por carrera
     */
    @Query("SELECT COUNT(c) FROM Curso c WHERE c.idCarrera = :idCarrera AND c.estatus = 'activo'")
    Long countCursosActivosByCarrera(@Param("idCarrera") Long idCarrera);

    /**
     * Obtiene el total de creditos por carrera
     */
    @Query("SELECT SUM(c.creditos) FROM Curso c WHERE c.idCarrera = :idCarrera AND c.estatus = 'activo'")
    Integer sumCreditosByCarrera(@Param("idCarrera") Long idCarrera);

    /**
     * Verifica si existe un curso con el codigo dado
     */
    boolean existsByCodigo(String codigo);
}
