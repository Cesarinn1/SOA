package com.uav.cursos.controller;

import com.uav.cursos.model.Curso;
import com.uav.cursos.service.CursoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Controlador REST para la gestion de Cursos
 * Expone los endpoints de la API RESTful
 */
@RestController
@RequestMapping("/api/cursos")
@Tag(name = "Cursos", description = "API para la gestion de cursos academicos")
@CrossOrigin(origins = "*")
public class CursoController {

    private final CursoService cursoService;

    @Autowired
    public CursoController(CursoService cursoService) {
        this.cursoService = cursoService;
    }

    /**
     * GET /api/cursos - Obtiene todos los cursos
     */
    @GetMapping
    @Operation(summary = "Listar todos los cursos", description = "Obtiene la lista completa de cursos registrados")
    @ApiResponse(responseCode = "200", description = "Lista de cursos obtenida exitosamente")
    public ResponseEntity<List<Curso>> listarTodos() {
        List<Curso> cursos = cursoService.obtenerTodos();
        return ResponseEntity.ok(cursos);
    }

    /**
     * GET /api/cursos/{id} - Obtiene un curso por ID
     */
    @GetMapping("/{id}")
    @Operation(summary = "Obtener curso por ID", description = "Obtiene un curso especifico por su ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Curso encontrado"),
        @ApiResponse(responseCode = "404", description = "Curso no encontrado")
    })
    public ResponseEntity<?> obtenerPorId(
            @Parameter(description = "ID del curso") @PathVariable Long id) {
        return cursoService.obtenerPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * GET /api/cursos/codigo/{codigo} - Obtiene un curso por codigo
     */
    @GetMapping("/codigo/{codigo}")
    @Operation(summary = "Obtener curso por codigo", description = "Obtiene un curso especifico por su codigo unico")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Curso encontrado"),
        @ApiResponse(responseCode = "404", description = "Curso no encontrado")
    })
    public ResponseEntity<?> obtenerPorCodigo(
            @Parameter(description = "Codigo del curso") @PathVariable String codigo) {
        return cursoService.obtenerPorCodigo(codigo)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * POST /api/cursos - Crea un nuevo curso
     */
    @PostMapping
    @Operation(summary = "Crear nuevo curso", description = "Registra un nuevo curso en el sistema")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Curso creado exitosamente"),
        @ApiResponse(responseCode = "400", description = "Datos invalidos")
    })
    public ResponseEntity<?> crear(@Valid @RequestBody Curso curso) {
        try {
            Curso nuevoCurso = cursoService.crear(curso);
            return ResponseEntity.status(HttpStatus.CREATED).body(nuevoCurso);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(crearError(e.getMessage()));
        }
    }

    /**
     * PUT /api/cursos/{id} - Actualiza un curso existente
     */
    @PutMapping("/{id}")
    @Operation(summary = "Actualizar curso", description = "Actualiza los datos de un curso existente")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Curso actualizado exitosamente"),
        @ApiResponse(responseCode = "404", description = "Curso no encontrado"),
        @ApiResponse(responseCode = "400", description = "Datos invalidos")
    })
    public ResponseEntity<?> actualizar(
            @Parameter(description = "ID del curso") @PathVariable Long id,
            @Valid @RequestBody Curso curso) {
        try {
            Curso cursoActualizado = cursoService.actualizar(id, curso);
            return ResponseEntity.ok(cursoActualizado);
        } catch (RuntimeException e) {
            if (e.getMessage().contains("no encontrado")) {
                return ResponseEntity.notFound().build();
            }
            return ResponseEntity.badRequest().body(crearError(e.getMessage()));
        }
    }

    /**
     * DELETE /api/cursos/{id} - Elimina un curso
     */
    @DeleteMapping("/{id}")
    @Operation(summary = "Eliminar curso", description = "Elimina un curso del sistema")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Curso eliminado exitosamente"),
        @ApiResponse(responseCode = "404", description = "Curso no encontrado")
    })
    public ResponseEntity<?> eliminar(
            @Parameter(description = "ID del curso") @PathVariable Long id) {
        try {
            cursoService.eliminar(id);
            Map<String, Object> response = new HashMap<>();
            response.put("mensaje", "Curso eliminado exitosamente");
            response.put("id", id);
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    /**
     * GET /api/cursos/carrera/{idCarrera} - Obtiene cursos por carrera
     */
    @GetMapping("/carrera/{idCarrera}")
    @Operation(summary = "Listar cursos por carrera", description = "Obtiene todos los cursos de una carrera especifica")
    public ResponseEntity<List<Curso>> obtenerPorCarrera(
            @Parameter(description = "ID de la carrera") @PathVariable Long idCarrera) {
        return ResponseEntity.ok(cursoService.obtenerPorCarrera(idCarrera));
    }

    /**
     * GET /api/cursos/semestre/{semestre} - Obtiene cursos por semestre
     */
    @GetMapping("/semestre/{semestre}")
    @Operation(summary = "Listar cursos por semestre", description = "Obtiene todos los cursos de un semestre especifico")
    public ResponseEntity<List<Curso>> obtenerPorSemestre(
            @Parameter(description = "Numero de semestre") @PathVariable Integer semestre) {
        return ResponseEntity.ok(cursoService.obtenerPorSemestre(semestre));
    }

    /**
     * GET /api/cursos/activos - Obtiene solo cursos activos
     */
    @GetMapping("/activos")
    @Operation(summary = "Listar cursos activos", description = "Obtiene todos los cursos con estatus activo")
    public ResponseEntity<List<Curso>> obtenerActivos() {
        return ResponseEntity.ok(cursoService.obtenerActivos());
    }

    /**
     * GET /api/cursos/buscar?nombre={nombre} - Busca cursos por nombre
     */
    @GetMapping("/buscar")
    @Operation(summary = "Buscar cursos por nombre", description = "Busca cursos que contengan el texto especificado en su nombre")
    public ResponseEntity<List<Curso>> buscarPorNombre(
            @Parameter(description = "Texto a buscar en el nombre") @RequestParam String nombre) {
        return ResponseEntity.ok(cursoService.buscarPorNombre(nombre));
    }

    /**
     * GET /api/cursos/carrera/{idCarrera}/semestre/{semestre} - Obtiene cursos por carrera y semestre
     */
    @GetMapping("/carrera/{idCarrera}/semestre/{semestre}")
    @Operation(summary = "Listar cursos por carrera y semestre",
               description = "Obtiene los cursos de una carrera y semestre especificos")
    public ResponseEntity<List<Curso>> obtenerPorCarreraYSemestre(
            @Parameter(description = "ID de la carrera") @PathVariable Long idCarrera,
            @Parameter(description = "Numero de semestre") @PathVariable Integer semestre) {
        return ResponseEntity.ok(cursoService.obtenerPorCarreraYSemestre(idCarrera, semestre));
    }

    /**
     * GET /api/cursos/estadisticas/carrera/{idCarrera} - Estadisticas de una carrera
     */
    @GetMapping("/estadisticas/carrera/{idCarrera}")
    @Operation(summary = "Estadisticas por carrera", description = "Obtiene estadisticas de cursos para una carrera")
    public ResponseEntity<Map<String, Object>> obtenerEstadisticasPorCarrera(
            @Parameter(description = "ID de la carrera") @PathVariable Long idCarrera) {
        Map<String, Object> estadisticas = new HashMap<>();
        estadisticas.put("idCarrera", idCarrera);
        estadisticas.put("totalCursosActivos", cursoService.contarCursosActivosPorCarrera(idCarrera));
        estadisticas.put("totalCreditos", cursoService.obtenerTotalCreditosPorCarrera(idCarrera));
        return ResponseEntity.ok(estadisticas);
    }

    /**
     * Crea un objeto de error estandarizado
     */
    private Map<String, String> crearError(String mensaje) {
        Map<String, String> error = new HashMap<>();
        error.put("error", mensaje);
        return error;
    }
}
