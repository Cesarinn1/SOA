package com.uav.cursos.service;

import com.uav.cursos.model.Curso;
import com.uav.cursos.repository.CursoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * Servicio para la gestion de Cursos
 * Contiene la logica de negocio para las operaciones CRUD
 */
@Service
@Transactional
public class CursoService {

    private final CursoRepository cursoRepository;

    @Autowired
    public CursoService(CursoRepository cursoRepository) {
        this.cursoRepository = cursoRepository;
    }

    /**
     * Obtiene todos los cursos
     */
    public List<Curso> obtenerTodos() {
        return cursoRepository.findAll();
    }

    /**
     * Obtiene un curso por su ID
     */
    public Optional<Curso> obtenerPorId(Long id) {
        return cursoRepository.findById(id);
    }

    /**
     * Obtiene un curso por su codigo
     */
    public Optional<Curso> obtenerPorCodigo(String codigo) {
        return cursoRepository.findByCodigo(codigo);
    }

    /**
     * Crea un nuevo curso
     */
    public Curso crear(Curso curso) {
        if (cursoRepository.existsByCodigo(curso.getCodigo())) {
            throw new RuntimeException("Ya existe un curso con el codigo: " + curso.getCodigo());
        }
        return cursoRepository.save(curso);
    }

    /**
     * Actualiza un curso existente
     */
    public Curso actualizar(Long id, Curso cursoActualizado) {
        return cursoRepository.findById(id)
                .map(curso -> {
                    curso.setCodigo(cursoActualizado.getCodigo());
                    curso.setNombre(cursoActualizado.getNombre());
                    curso.setDescripcion(cursoActualizado.getDescripcion());
                    curso.setCreditos(cursoActualizado.getCreditos());
                    curso.setHorasTeoricas(cursoActualizado.getHorasTeoricas());
                    curso.setHorasPracticas(cursoActualizado.getHorasPracticas());
                    curso.setIdCarrera(cursoActualizado.getIdCarrera());
                    curso.setSemestre(cursoActualizado.getSemestre());
                    curso.setEstatus(cursoActualizado.getEstatus());
                    return cursoRepository.save(curso);
                })
                .orElseThrow(() -> new RuntimeException("Curso no encontrado con ID: " + id));
    }

    /**
     * Elimina un curso por su ID
     */
    public void eliminar(Long id) {
        if (!cursoRepository.existsById(id)) {
            throw new RuntimeException("Curso no encontrado con ID: " + id);
        }
        cursoRepository.deleteById(id);
    }

    /**
     * Obtiene cursos por carrera
     */
    public List<Curso> obtenerPorCarrera(Long idCarrera) {
        return cursoRepository.findByIdCarrera(idCarrera);
    }

    /**
     * Obtiene cursos por semestre
     */
    public List<Curso> obtenerPorSemestre(Integer semestre) {
        return cursoRepository.findBySemestre(semestre);
    }

    /**
     * Obtiene cursos activos
     */
    public List<Curso> obtenerActivos() {
        return cursoRepository.findByEstatus(Curso.EstatusCurso.activo);
    }

    /**
     * Busca cursos por nombre
     */
    public List<Curso> buscarPorNombre(String nombre) {
        return cursoRepository.findByNombreContaining(nombre);
    }

    /**
     * Obtiene cursos por carrera y semestre
     */
    public List<Curso> obtenerPorCarreraYSemestre(Long idCarrera, Integer semestre) {
        return cursoRepository.findByIdCarreraAndSemestre(idCarrera, semestre);
    }

    /**
     * Cuenta cursos activos por carrera
     */
    public Long contarCursosActivosPorCarrera(Long idCarrera) {
        return cursoRepository.countCursosActivosByCarrera(idCarrera);
    }

    /**
     * Obtiene total de creditos por carrera
     */
    public Integer obtenerTotalCreditosPorCarrera(Long idCarrera) {
        Integer total = cursoRepository.sumCreditosByCarrera(idCarrera);
        return total != null ? total : 0;
    }
}
