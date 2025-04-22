import numpy as np
import sapien.core as sapien

def debug_robot_dofs():
    # Initialize SAPIEN
    engine = sapien.Engine()
    renderer = sapien.VulkanRenderer()
    engine.set_renderer(renderer)
    
    scene = engine.create_scene()
    
    # Load the UR3e robot
    loader = scene.create_urdf_loader()
    urdf_path = "/home/shreya/Desktop/gendp/sapien_env/sapien_env/assets/robot/ur_description/ur3e.urdf"
    robot = loader.load(urdf_path)
    
    if robot is None:
        print("Failed to load robot!")
        return
    
    # Print robot information
    print(f"Robot total DOF: {robot.dof}")
    
    # Print active joint information
    print("\nActive joints:")
    for i, joint in enumerate(robot.get_active_joints()):
        print(f"  [{i}] {joint.get_name()}: {joint.get_dof()} DOF, Type: {joint.type}, Limits: {joint.get_limits()}")
    
    # Print qpos structure
    qpos = robot.get_qpos()
    print(f"\nqpos shape: {qpos.shape}, values: {qpos}")
    
    # Test setting qpos
    new_qpos = np.zeros_like(qpos)
    # Set arm joints to a reasonable position
    if len(new_qpos) >= 6:
        new_qpos[:6] = [0, -1.57, 1.57, -1.57, -1.57, 0]
        
    # Try to open the gripper by setting the finger position(s)
    if len(new_qpos) > 6:
        for i in range(6, len(new_qpos)):
            new_qpos[i] = 0.025  # Fully open
    
    print(f"\nSetting new qpos: {new_qpos}")
    robot.set_qpos(new_qpos)
    print(f"After set_qpos, actual qpos: {robot.get_qpos()}")
    
    # Check which links actually moved
    print("\nLink positions after setting qpos:")
    for link in robot.get_links():
        if "finger" in link.get_name():
            print(f"  {link.get_name()}: {link.get_pose().p}")

if __name__ == "__main__":
    debug_robot_dofs()