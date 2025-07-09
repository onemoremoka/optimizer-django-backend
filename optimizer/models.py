from django.db import models

# Create your models here.

# Aqui defino la estructura de la base de datos (similar a pydantic pero de django)
class OptimizationResult(models.Model):
    product_a = models.FloatField()
    product_b = models.FloatField()
    objective_value = models.FloatField()
    machine_1_lhs = models.FloatField()
    machine_1_rhs = models.FloatField()
    machine_2_lhs = models.FloatField()
    machine_2_rhs = models.FloatField()
    status = models.CharField(max_length=10)
    termination = models.CharField(max_length=10)
    solve_time = models.FloatField()
    error_rc = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result at {self.timestamp}"